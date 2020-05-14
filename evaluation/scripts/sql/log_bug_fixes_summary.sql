COPY (
	SELECT DISTINCT On (change_summary.sha) change_summary.sha, 
			change_summary.project, 
			author, 
			author_email, 
			commit_date, 
			is_bug 
	FROM   change_summary 
	       INNER JOIN method_change_detail 
		       ON method_change_detail.sha = change_summary.sha 
	WHERE  change_summary.is_bug 
	       AND ( "info__ctxt" > 0 
			OR "config__ctxt" > 0 
			OR "fine__ctxt" > 0 
			OR "finer__ctxt" > 0 
			OR "finest__ctxt" > 0 
			OR "severe__ctxt" > 0 
			OR "warning__ctxt" > 0 
			OR "error__ctxt" > 0 
			OR "warn__ctxt" > 0 
			OR "debug__ctxt" > 0 
			OR "trace__ctxt" > 0 
			OR "log__ctxt" > 0 
			OR "logp__ctxt" > 0 
			OR "logrb__ctxt" > 0 
		) 
	ORDER  BY change_summary.sha, 
		  change_summary.project DESC, 
		  file_name, 
		  method_name 
) TO STDOUT with CSV HEADER
