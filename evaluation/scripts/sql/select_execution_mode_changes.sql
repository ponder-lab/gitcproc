SELECT method_change_detail.project, 
       method_change_detail.sha, 
       method_change_detail.language, 
       method_change_detail.file_name, 
       method_change_detail.is_test, 
       method_change_detail.method_name, 
       method_change_detail.parallel_adds, 
       method_change_detail.parallel_dels, 
       method_change_detail.parallelstream_adds, 
       method_change_detail.parallelstream_dels, 
       method_change_detail.sequential_adds, 
       method_change_detail.sequential_dels, 
       method_change_detail.total_adds, 
       method_change_detail.total_dels, 
       method_change_detail.warning_alert, 
       change_summary.is_bug 
FROM   method_change_detail 
       INNER JOIN change_summary 
               ON method_change_detail.sha = change_summary.sha 
WHERE  method_change_detail.parallel_adds > 0 
        OR method_change_detail.parallel_dels > 0 
        OR method_change_detail.sequential_adds > 0 
        OR method_change_detail.sequential_dels > 0 
        OR parallelstream_adds > 0 
        OR method_change_detail.parallelstream_dels > 0 
ORDER  BY method_change_detail.project DESC, 
          method_change_detail.sha, 
          file_name, 
          method_name 
