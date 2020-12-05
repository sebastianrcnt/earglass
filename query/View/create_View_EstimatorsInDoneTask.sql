-- estimators in done task

create definer = earglass@`%` view EstimatorsInDoneTask as
select distinct `E`.`FK_idEstimator`                             AS `FK_idEstimator`,
                row_number() over ( partition by `T`.`TaskName`) AS `IndexNum`,
                `T`.`TaskName`                                   AS `TaskName`
from `earglass`.`TASK` `T`
         join `earglass`.`EVALUATION` `E`
         join `earglass`.`PARSING_DSF` `P`
where `T`.`Status` = 'done'
  and `T`.`TaskName` = `P`.`TaskName`
  and `P`.`idPARSING_DSF` = `E`.`FK_idPARSING_DSF`
  and `E`.`Status` = 'done'
group by `E`.`FK_idEstimator`, `T`.`TaskName`;



