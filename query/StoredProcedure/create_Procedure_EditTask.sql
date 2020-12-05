create
    definer = earglass@`%` procedure EditTask(IN currentTaskName varchar(45), IN newDescription text,
                                              IN newMinPeriod int, IN newMaxDuplicatedRowRatio float,
                                              IN newMaxNullRatioPerColumn float, IN newPassCriteria text)
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
            AS EditTaskErrorMessage;
            ROLLBACK;
        LEAVE checkrow;
    END IF;

	-- if (varRowCount = 1) then task exists in database.
    IF (varRowCount = 1) THEN
        UPDATE TASK
        SET Description = newDescription, MinPeriod = newMinPeriod,
            MaxDuplicatedRowRatio = newMaxDuplicatedRowRatio,
            MaxNullRatioPerColumn = newMaxNullRatioPerColumn,
            PassCriteria = newPassCriteria
        WHERE TaskName = currentTaskName;

        SELECT 'Edit task info successfully'
            AS EditTaskSuccessMessage;

    END IF;

-- END checkrow
END checkrow;

