create
    definer = team9@`%` procedure UpdateUserInfo(IN varId varchar(45), IN newPassword varchar(45),
                                                    IN newName varchar(45), IN newBirthDate varchar(8),
                                                    IN newPhoneNum varchar(13), IN newAddress varchar(100))
checkexist:BEGIN

    DECLARE varRowCount     Varchar(45);

    -- check if varId exists in database
    SELECT COUNT(*) INTO varRowCount
    FROM USER
    WHERE id = varID;

    -- if (varRowCount != 1) then user does not exist.
    IF (varRowCount != 1) THEN
        -- Print message
        SELECT 'User ID does not exists.'
            AS UpdateUserInfoErrorMessage;
            ROLLBACK;
        LEAVE checkexist;
    END IF;

    -- if (varRowCount = 1) then user exists in database.
    IF (varRowCount = 1) THEN
        -- Update User info.
	    UPDATE USER
            SET Password = newPassword,
                Name = newName,
                BirthDate = newBirthDate,
                PhoneNum = newPhoneNum,
                Address = newAddress
            WHERE Id = varId;

        SELECT 'Modify User Info successfully'
            AS UpdateUserInfoSuccessMessage;
    END IF;
-- END checkexist
END checkexist;

