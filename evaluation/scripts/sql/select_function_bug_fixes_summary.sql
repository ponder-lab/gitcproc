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
	       AND ( "tf.function_adds" > 0 
		      OR "tf.function_dels" > 0 ) 
	ORDER  BY change_summary.sha, 
		  change_summary.project DESC, 
		  file_name, 
		  method_name 
) TO STDOUT with CSV HEADER
