create
    definer = team9@`%` procedure InsertNewTask(IN newTaskName varchar(45), IN newDescription text,
                                                   IN newMinPeriod int, IN newTaskDataTableName varchar(100),
                                                   IN newMaxDuplicatedRowRatio float, IN newMaxNullRatioPerColumn float,
                                                   IN newPassCriteria text, IN newTaskDataTableSchemaInfo text)
checkdupli:BEGIN

    DECLARE varRowCount  Int;
    DECLARE varIdManager Int;

    -- check to see if varTaskName exist in database
    SELECT COUNT(*) INTO varRowCount
    FROM TASK
    WHERE TaskName = newTaskName;


    -- if (varRowCount > 0) then task already exits.
    IF (varRowCount > 0) THEN
        -- Print message
        SELECT 'Task name already exists.'
            AS InsertNewTaskErrorMessage;
            ROLLBACK;
        LEAVE checkdupli;
    END IF;

	-- if (varRowCount = 0) then task does not exist in database.
    IF (varRowCount = 0) THEN
        -- get idUSER surrogate key value, check for validity.
        SELECT idUSER INTO varIdManager
        FROM USER
        WHERE FK_UserTypeName = '관리자';

        -- Insert new Customer data.
	    INSERT INTO TASK (TaskName, Description, MinPeriod, Status,
        TaskDataTableName, FK_idManager, MaxDuplicatedRowRatio,
        MaxNullRatioPerColumn, PassCriteria, TaskDataTableSchemaInfo)
           VALUES(newTaskName, newDescription,
		  		  newMinPeriod, 'ongoing', newTaskDataTableName,
                    varIdManager, newMaxDuplicatedRowRatio,
                    newMaxNullRatioPerColumn, newPassCriteria, newTaskDataTableSchemaInfo);

        SELECT 'Insert new task successfully'
            AS InsertNewTaskSuccessMessage;
        
    END IF;
-- END checkdupli
END checkdupli;

