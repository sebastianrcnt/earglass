-- submitters in done task

CREATE VIEW SubmittersInDoneTask AS
    SELECT DISTINCT P.SubmitterId, ROW_NUMBER() over (PARTITION BY T.TaskName) AS IndexNum, T.TaskName
    FROM PARSING_DSF AS P, TASK AS T
    WHERE T.Status = 'done'
    AND T.TaskName = P.TaskName
    AND P.SubmitNum = 1;


