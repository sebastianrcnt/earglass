create
    definer = team9@`%` procedure UpdateParticipationStatus(IN varFK_TaskName varchar(45), IN varFK_idUSER int,
                                                               IN newStatus varchar(45), IN newComment text)
BEGIN
    IF (newStatus = 'ongoing' or newStatus = 'reject') THEN
        -- If exists participation row
        IF EXISTS
        (SELECT * FROM PARTICIPATION
         WHERE  PARTICIPATION.FK_TaskName = varFK_TaskName
            AND PARTICIPATION.FK_idUSER = varFK_idUSER
            AND PARTICIPATION.status = 'waiting') THEN
            -- update participation status to accpted or rejected
            UPDATE PARTICIPATION
                SET     PARTICIPATION.Status = newStatus,
                        PARTICIPATION.Comment = newComment
                WHERE   (PARTICIPATION.FK_TaskName = varFK_TaskName
                    AND  PARTICIPATION.FK_idUSER = varFK_idUSER);
        END IF;
        -- print message
        SELECT 'update participation status successfully'
        AS UpdateParticipationStausResults;

    ELSE
        -- print message
        SELECT 'Invalid participation status value'
        AS UpdateParticipationStatusErrorMessage;
    END IF;
END;

