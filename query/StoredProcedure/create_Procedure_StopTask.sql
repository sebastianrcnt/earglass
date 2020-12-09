create
    definer = team9@`%` procedure StopTask(IN currentTaskName varchar(45))
checkrow:BEGIN

    DECLARE varRowCount     Int;

    -- check to see if currentTaskName exist in database
    SELECT COUNT(*) INTO varRowCount
    FROM TASK
    WHERE TaskName = currentTaskName;

    -- if (varRowCount = 0) then task does not exist in database.
    IF (varRowCount = 0) THEN
        -- Print message
        SELECT 'Task name does not exist.'
            AS StopTaskErrorMessage;
            ROLLBACK;
        LEAVE checkrow;
    END IF;

	-- if (varRowCount = 1) then task exists in database.
    IF (varRowCount = 1) THEN

        UPDATE TASK
            SET Status = 'done'
            WHERE TaskName = currentTaskName;
        
        UPDATE PARTICIPATION
            SET Status = 'done'
            WHERE FK_TaskName = currentTaskName;
        
        UPDATE EVALUATION
            SET Status = 'notEstimated',
                EndTime = NOW()
            WHERE FK_idPARSING_DSF IN (SELECT idPARSING_DSF
                                        FROM PARSING_DSF
                                        WHERE TaskName = currentTaskName)
            AND Score IS NULL;

        UPDATE PARSING_DSF
            SET TotalStatus = 'notEstimated'
            WHERE AverageScore is NULL
            AND TaskName = currentTaskName;

        UPDATE PARSING_DSF
            SET TotalStatus = 'done'
            WHERE TotalScore is not NULL
            AND TaskName = currentTaskName;
        
        SELECT 'Stopping task successfully'
            AS StopTaskSuccessMessage;

    END IF;

-- END checkrow
END checkrow;

