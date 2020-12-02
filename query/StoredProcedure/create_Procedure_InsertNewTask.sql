-- 관리자가 task table에 정보 insert
-- taskname, description, 최소업로드주기, table 이름, 스키마, 원본 데이터 타입,
-- 시스템 pass 기준, 평가자 pass 기준

DELIMITER //

CREATE PROCEDURE InsertNewTask
            (IN newTaskName             Varchar(45),
             IN newDescription          Varchar(45),
             IN newMinPeriod            Int(11),
             IN newTaskDataTableName    varchar(100),
             IN newMaxDuplicatedRowRatio    Float,
             IN newMaxNullRatioPerColumn    Float,
             IN newPassCriteria             text,
             IN newTaskDataTableSchemaInfo  text)

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
    inserttask:BEGIN
	    -- Rollback everything if unable to complete it.
	    START TRANSACTION;

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

      -- END inserttask
    END inserttask;
    END IF;
-- END checkdupli
END checkdupli
//

DELIMITER ;
