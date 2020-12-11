select
	mcd.project,
	mcd.sha,
	cs.author,
	cs.author_email,
	cs.commit_date,
	cs.is_bug,
	mcd.language,
	mcd.file_name,
	mcd.is_test,
	mcd.method_name,
	mcd."tf.function_adds",
	mcd."tf.function_dels",
	mcd.total_adds,
	mcd.total_dels,
	mcd.warning_alert
from method_change_detail as mcd
	inner join change_summary as cs
		on mcd.sha = cs.sha
where
	mcd."tf.function_adds" > 0 or 
	mcd."tf.function_dels" > 0
order by
	cs.project desc,
	file_name,
	method_name