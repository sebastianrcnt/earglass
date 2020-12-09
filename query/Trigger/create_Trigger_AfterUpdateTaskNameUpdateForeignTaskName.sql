create definer = team9@`%` trigger AfterUpdateTaskNameUpdateForeignTaskName
    after update
    on TASK
    for each row
BEGIN

    UPDATE PARSING_DSF
    SET TaskName = NEW.TaskName
    WHERE TaskName = OLD.TaskName;
END;

