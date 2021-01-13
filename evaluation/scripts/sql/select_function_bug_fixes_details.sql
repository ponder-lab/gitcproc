COPY (
	SELECT method_change_detail.* 
	FROM   method_change_detail 
	       INNER JOIN change_summary 
		       ON method_change_detail.sha = change_summary.sha 
	WHERE  change_summary.is_bug 
	       AND ( "tf.function_adds" > 0 
		      OR "tf.function_dels" > 0 ) 
	ORDER  BY method_change_detail.project DESC, 
		  method_change_detail.sha, 
		  file_name, 
		  method_name 
) TO STDOUT with CSV HEADER
