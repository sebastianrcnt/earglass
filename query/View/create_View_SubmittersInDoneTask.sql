-- submitters in done task

create definer = earglass@`%` view SubmittersInDoneTask as
select distinct `P`.`SubmitterID`                                AS `SubmitterId`,
                row_number() over ( partition by `T`.`TaskName`) AS `IndexNum`,
                `T`.`TaskName`                                   AS `TaskName`
from `earglass`.`PARSING_DSF` `P`
         join `earglass`.`TASK` `T`
where `T`.`Status` = 'done'
  and `T`.`TaskName` = `P`.`TaskName`
  and `P`.`SubmitNum` = 1;



