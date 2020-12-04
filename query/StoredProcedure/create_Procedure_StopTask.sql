-- 관리자가 task를 강제 종료 하면 모든 TABLE의  status를 done으로 업데이트

DELIMITER //

CREATE PROCEDURE StopTask
            (IN currentTaskName             Varchar(45))

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

        UPDATE EVALUATION
            SET Status = 'notEstimated',
                EndTime = NOW()
            WHERE FK_idPARSING_DSF IN (SELECT idPARSING_DSF
                                        FROM PARSING_DSF
                                        WHERE TaskName = currentTaskName)
            AND (Score IS NULL
            OR Pass IS NULL);

        UPDATE PARSING_DSF
            SET TotalStatus = 'notEstimated'
            WHERE (AverageScore is NULL
            OR Pass is NULL)
            AND TaskName = currentTaskName;

        UPDATE PARSING_DSF
            SET TotalStatus = 'done'
            WHERE TotalScore is not NULL
            AND Pass is not NULL
            AND TaskName = currentTaskName;

        UPDATE PARTICIPATION
            SET Status = 'done'
            WHERE FK_TaskName = currentTaskName;

        SELECT 'Stopping task successfully'
            AS StopTaskSuccessMessage;

    END IF;

-- END checkrow
END checkrow
//

DELIMITER ;
