create definer = team9@`%` trigger AfterInsertParsingDSFInsertEvaluation
    after insert
    on PARSING_DSF
    for each row
triggers: Begin

	DECLARE varEstimatorNum INT(11);
	DECLARE varIndexNum INT(11);
	DECLARE varEstimatorID INT(11);
	DECLARE varidPARSING_DSF INT(11);

	SET varidPARSING_DSF = NEW.idPARSING_DSF;

	SELECT COUNT(*) INTO varEstimatorNum
	FROM USER
	WHERE FK_UserTypeName = '평가자';
	IF varEstimatorNum = 0 THEN
		LEAVE triggers;
	END IF;

	DROP TEMPORARY TABLE IF EXISTS RandomEstimatorIDs;

	CREATE TEMPORARY TABLE RandomEstimatorIDs AS
	    SELECT *
	    FROM RandomEstimatorID;

	IF varEstimatorNum < 3 THEN
		SET varIndexNum = 0;

		myloop: LOOP
			SET varIndexNum = varIndexNum + 1;

			SELECT idUSER INTO varEstimatorID
			FROM RandomEstimatorIDs
			WHERE IndexNum = varIndexNum;

			INSERT INTO EVALUATION
			(FK_idPARSING_DSF, FK_idEstimator, StartTime, Deadline)
			VALUES (varidPARSING_DSF, varEstimatorID, NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY));

			IF varIndexNum = varEstimatorNum THEN
				LEAVE myloop;
			END IF;
		END LOOP myloop;

	ELSE
		SET varIndexNum = 0;
		myloop2: LOOP
			SET varIndexNum = varIndexNum + 1;
			SELECT idUSER INTO varEstimatorID
			FROM RandomEstimatorIDs
			WHERE IndexNum = varIndexNum;

			INSERT INTO EVALUATION
			(FK_idPARSING_DSF, FK_idEstimator, StartTime, Deadline)
			VALUES (varidPARSING_DSF, varEstimatorID, NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY));

			IF varIndexNum = 3 THEN
				LEAVE myloop2;
			END IF;
		END LOOP myloop2;
	END IF;

END triggers;

