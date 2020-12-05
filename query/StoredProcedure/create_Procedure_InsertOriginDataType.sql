create
    definer = earglass@`%` procedure InsertOriginDataType(IN currTaskName varchar(45), IN newDataTypeName varchar(45),
                                                          IN newSchemaInfo varchar(1000), IN newMappingInfo longtext)
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
END checkexist;

