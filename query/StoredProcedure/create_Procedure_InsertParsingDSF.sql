create
    definer = team9@`%` procedure InsertParsingDSF(IN newTaskName varchar(45), IN newParsingFile longtext,
                                                      IN newOriginDataTypeID int, IN newSubmitterID int,
                                                      IN newPeriod varchar(45), IN newFK_idORIGIN_DSF int,
                                                      IN newRound int, IN newSystemScore float)
checkexist:BEGIN

    DECLARE varidORIGIN_DSF Int(11);
    DECLARE varSubmitNum    Int(11);

    -- check if origin_dsf exists
    SELECT COUNT(*) INTO varidORIGIN_DSF
    FROM ORIGIN_DSF
    WHERE idORIGIN_DSF = newFK_idORIGIN_DSF;

    IF varidORIGIN_DSF = 0
    THEN SELECT 'Origin DSF does not exist'
            AS OriginDSFErrorMessage;
            ROLLBACK;
        Leave checkexist;
    END IF;

    SELECT COUNT(*) INTO varSubmitNum
    FROM PARSING_DSF
    WHERE TaskName = newTaskName AND SubmitterID = newSubmitterID;

    IF (varSubmitNum = 0) THEN
        INSERT INTO PARSING_DSF (TaskName, ParsingFile, OriginDataTypeID, SubmitterID, SubmitNum, Period, TotalStatus, FK_idORIGIN_DSF, Round, SystemScore)
        VALUES (newTaskName, newParsingFile, newOriginDataTypeID, newSubmitterID, 1, newPeriod, 'ongoing', newFK_idORIGIN_DSF, newRound, newSystemScore);
        SELECT LAST_INSERT_ID();
    ELSE
        INSERT INTO PARSING_DSF (TaskName, ParsingFile, OriginDataTypeID, SubmitterID, SubmitNum, Period, TotalStatus, FK_idORIGIN_DSF, Round, SystemScore)
        VALUES (newTaskName, newParsingFile, newOriginDataTypeID, newSubmitterID, varSubmitNum+1, newPeriod, 'ongoing', newFK_idORIGIN_DSF, newRound, newSystemScore);
        SELECT LAST_INSERT_ID();
    END IF;

-- END checkexist
END checkexist;

