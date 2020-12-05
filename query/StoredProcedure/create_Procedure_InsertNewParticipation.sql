create
    definer = earglass@`%` procedure InsertNewParticipation(IN newFK_TaskName varchar(45), IN newFK_idUSER int)
checkexist: BEGIN
    IF EXISTS (SELECT * FROM PARTICIPATION
                WHERE FK_TaskName = newFK_TaskName
                AND FK_idUSER = newFK_idUSER) THEN
            SELECT 'already parcitipate'
            AS InsertNewParticipationErrorMessage;
            ROLLBACK;
        LEAVE checkexist;
    END IF;

    INSERT INTO PARTICIPATION (FK_TaskName, FK_idUSER, Status)
        VALUES(newFK_TaskName, newFK_idUSER, 'waiting');

END;

