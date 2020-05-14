COPY (
	SELECT method_change_detail.* 
	FROM   method_change_detail 
	       INNER JOIN change_summary 
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
			OR "logrb__ctxt" > 0 ) 
	ORDER  BY method_change_detail.project DESC, 
		  method_change_detail.sha, 
		  file_name, 
		  method_name 
) TO STDOUT with CSV HEADER
