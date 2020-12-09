-- estimators in done task

create definer = team9@`%` view EstimatorsInDoneTask as
select distinct `E`.`FK_idEstimator`                             AS `FK_idEstimator`,
                row_number() over ( partition by `T`.`TaskName`) AS `IndexNum`,
                `T`.`TaskName`                                   AS `TaskName`
from `team9`.`TASK` `T`
         join `team9`.`EVALUATION` `E`
         join `team9`.`PARSING_DSF` `P`
where `T`.`Status` = 'done'
  and `T`.`TaskName` = `P`.`TaskName`
  and `P`.`idPARSING_DSF` = `E`.`FK_idPARSING_DSF`
  and `E`.`Status` = 'done'
group by `E`.`FK_idEstimator`, `T`.`TaskName`;



