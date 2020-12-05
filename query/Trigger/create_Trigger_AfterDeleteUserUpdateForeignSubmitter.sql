create definer = earglass@`%` trigger AfterDeleteUserUpdateForeignSubmitter
    after delete
    on USER
    for each row
BEGIN

    UPDATE PARSING_DSF
    SET SubmitterID = NULL
    WHERE SubmitterID = OLD.idUSER;
END;

