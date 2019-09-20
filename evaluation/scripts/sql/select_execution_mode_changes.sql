COPY (
	SELECT method_change_detail.project, 
	       method_change_detail.sha, 
	       method_change_detail.language, 
	       method_change_detail.file_name, 
	       method_change_detail.is_test, 
	       method_change_detail.method_name, 
	       method_change_detail.parallel___adds, 
	       method_change_detail.parallel___dels, 
	       method_change_detail."parallelStream___adds", 
	       method_change_detail."parallelStream___dels", 
	       method_change_detail.sequential___adds, 
	       method_change_detail.sequential___dels, 
	       method_change_detail.total_adds, 
	       method_change_detail.total_dels, 
	       method_change_detail.warning_alert, 
	       change_summary.is_bug 
	FROM   method_change_detail 
	       INNER JOIN change_summary 
		       ON method_change_detail.sha = change_summary.sha 
	WHERE  method_change_detail.parallel___adds > 0
		OR method_change_detail.parallel___dels > 0
		OR method_change_detail.sequential___adds > 0
		OR method_change_detail.sequential___dels > 0
		OR method_change_detail."parallelStream___adds" > 0
		OR method_change_detail."parallelStream___dels" > 0
	ORDER  BY method_change_detail.project DESC,
		  method_change_detail.sha,
		  file_name,
		  method_name
) TO STDOUT with CSV HEADER
