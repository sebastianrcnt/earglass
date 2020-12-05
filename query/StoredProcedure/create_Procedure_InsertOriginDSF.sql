create
    definer = earglass@`%` procedure InsertOriginDSF(IN newOriginFile longtext, IN newPeriod varchar(45),
                                                     IN newFK_TaskName varchar(45), IN newFK_idUSER int,
                                                     IN newFK_idORIGIN_DATA_TYPE int, IN newRound int)
checkexist:BEGIN

    DECLARE varSubmitNum    Int(11);

    -- check if Participation exists
    IF (SELECT Status
    FROM PARTICIPATION
    WHERE FK_TaskName = newFK_TaskName and FK_idUSER = newFK_idUSER) != 'ongoing'
    THEN SELECT 'Participation does not exist'
            AS ParticipationErrorMessage;
            ROLLBACK;
        Leave checkexist;
    END IF;


    SELECT COUNT(*) INTO varSubmitNum
    FROM ORIGIN_DSF
    WHERE FK_TaskName = newFK_TaskName AND FK_idUSER = newFK_idUSER;

    IF (varSubmitNum = 0) THEN
        INSERT INTO ORIGIN_DSF (OriginFile, SubmitNum, DateTime, Period, FK_TaskName, FK_idUSER, FK_idORIGIN_DATA_TYPE, Round)
        VALUES (newOriginFile, 1, NOW(), newPeriod, newFK_TaskName, newFK_idUSER, newFK_idORIGIN_DATA_TYPE, newRound);
        SELECT LAST_INSERT_ID();
    ELSE
        INSERT INTO ORIGIN_DSF (OriginFile, SubmitNum, DateTime, Period, FK_TaskName, FK_idUSER, FK_idORIGIN_DATA_TYPE, Round)
        VALUES (newOriginFile, varSubmitNum+1, NOW(), newPeriod, newFK_TaskName, newFK_idUSER, newFK_idORIGIN_DATA_TYPE, newRound);
        SELECT LAST_INSERT_ID();
    END IF;

-- END checkexist
END checkexist;

