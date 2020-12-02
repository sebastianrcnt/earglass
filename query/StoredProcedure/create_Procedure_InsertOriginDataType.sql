-- 원본 데이터 타입 추가

DELIMITER //

CREATE PROCEDURE InsertOriginDataType
            (IN currTaskName                 Varchar(45),
             IN newDataTypeName             Varchar(45),
             IN newSchemaInfo               Varchar(1000),
             IN newMappingInfo              LONGTEXT)

checkexist:BEGIN

    DECLARE varSubmitNum    Int(11);

    -- check if task name exists
    IF NOT EXISTS (SELECT * FROM TASK
            WHERE TaskName = currTaskName and Status = 'ongoing') THEN
        SELECT 'Invalid Task Name'
        AS InsertOriginDataTypeErrorMessage;
        ROLLBACK;
    LEAVE checkexist;
    END IF;
    
    INSERT INTO ORIGIN_DATA_TYPE (TaskName, SchemaInfo, MappingInfo, DataTypeName)
        VALUES (currTaskName, newSchemaInfo, newMappingInfo, newDataTypeName);

-- END checkexist
END checkexist
//

DELIMITER ;
