create
    definer = team9@`%` procedure DeleteUser(IN curId varchar(45), IN curPassword varchar(45))
checkrow:BEGIN

    DECLARE RowCount     Varchar(45);

    -- check if varPassword matches user's password
    SELECT COUNT(*) INTO RowCount
    FROM USER
    WHERE Id = curId AND Password = curPassword;

    -- if ID does not exist in database
    IF (RowCount = 0) THEN
        SELECT 'Wrong Password'
            AS WrongPasswordErrorMessage;
            ROLLBACK;
        LEAVE checkrow;
    END IF;

    -- if password matches then delete user from the table
    IF (RowCount = 1) THEN
        DELETE FROM USER
        WHERE Id = CurId;

        SELECT 'You have successfully left our service.'
            AS DeleteUserSuccessMessage;

    END IF;
-- END checkrow
END checkrow;

