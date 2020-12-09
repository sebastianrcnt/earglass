create definer = team9@`%` trigger AfterEvaluationUpdateParsingDSFScores
    after update
    on EVALUATION
    for each row
Begin

		DECLARE varidEVALUATION int(11);
		DECLARE varidPARSING_DSF int(11);
		DECLARE varScoreSum int(11);
		DECLARE varAverageScore float;
		DECLARE varPassCount int(11);
		DECLARE varNonPassCount int(11);
		DECLARE varTotalPass varchar(45);
		DECLARE varEvaluationNum int(11);

		SET varidEVALUATION = NEW.idEVALUATION;
		SET varidPARSING_DSF = NEW.FK_idPARSING_DSF;
		SET varPassCount = 0;
		SET varNonPassCount = 0;

		IF NEW.Status = 'done' THEN
			SELECT SUM(E.Score * U.UserScore) INTO varScoreSum
			FROM EVALUATION AS E, USER AS U
			WHERE E.FK_idEstimator = U.idUSER
			AND E.FK_idPARSING_DSF = varidPARSING_DSF
			AND E.Score IS NOT NULL;
			
			SELECT COUNT(E.idEVALUATION) INTO varEvaluationNum
			FROM EVALUATION AS E
			WHERE E.FK_idPARSING_DSF = varidPARSING_DSF
			AND E.Score IS NOT NULL;

			SET varAverageScore = varScoreSum / (60*varEvaluationNum);
            IF varAverageScore > 100 THEN
                SET varAverageScore = 100;
            END IF;

			SELECT COUNT(*) INTO varPassCount
			FROM EVALUATION
			WHERE FK_idPARSING_DSF = varidPARSING_DSF
			AND Pass = 'P';

			SELECT COUNT(*) INTO varNonPassCount
			FROM EVALUATION
			WHERE FK_idPARSING_DSF = varidPARSING_DSF
			AND Pass = 'NP';

			IF (varPassCount - varNonPassCount) > 0 THEN
				SET varTotalPass = 'P';
			ELSE
				SET varTotalPass = 'NP';
			END IF;

			UPDATE PARSING_DSF
			SET AverageScore = varAverageScore,
				TotalScore = 0.4*SystemScore + 0.6*varAverageScore,
				Pass = varTotalPass
			WHERE idPARSING_DSF = varidPARSING_DSF;

		END IF;

END;

