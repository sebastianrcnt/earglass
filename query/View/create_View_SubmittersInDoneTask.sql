-- submitters in done task

create definer = team9@`%` view SubmittersInDoneTask as
select distinct `P`.`SubmitterID`                                AS `SubmitterId`,
                row_number() over ( partition by `T`.`TaskName`) AS `IndexNum`,
                `T`.`TaskName`                                   AS `TaskName`
from `team9`.`PARSING_DSF` `P`
         join `team9`.`TASK` `T`
where `T`.`Status` = 'done'
  and `T`.`TaskName` = `P`.`TaskName`
  and `P`.`SubmitNum` = 1;



