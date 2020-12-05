create definer = earglass@`%` trigger AfterTaskDoneUpdateEstimatorScore
    after update
    on TASK
    for each row
BEGIN
    DECLARE curTaskName             varchar(45);
    DECLARE varIndex               INT(11);
    DECLARE varEstimatorNum        INT(11);
    DECLARE varFK_idEstimator       INT(11);
    DECLARE varFileNum              INT(11);
    DECLARE varEvaluationNum        INT(11);
    DECLARE varAvgScore             FLOAT;
    DECLARE varSTDScore             FLOAT;
    DECLARE varSmallIndex           INT(11);
    DECLARE varNormZ                FLOAT;
    DECLARE varOutlierCount          INT(11);
    DECLARE varGoodEvaluationNum    INT(11);
    DECLARE newEstimatorScore       FLOAT;
    DECLARE currUserScore           Float;

    SET curTaskName = NEW.TaskName;
    SET varIndex = 0;
    IF (NEW.Status = 'done') THEN

        SELECT  COUNT(*) INTO varEstimatorNum
        FROM EstimatorsInDoneTask
        WHERE TaskName = curTaskName LIMIT 1;

        myloop: LOOP
            SET varIndex = varIndex + 1;

            SELECT FK_idEstimator INTO varFK_idEstimator
            FROM EstimatorsInDoneTask
            WHERE TaskName = curTaskName
            AND IndexNum = varIndex;

            -- 배정 개수 계산
            SELECT COUNT(*) INTO varFileNum
            FROM EVALUATION
            WHERE FK_idEstimator = varFK_idEstimator
            AND FK_idPARSING_DSF IN (SELECT idPARSING_DSF
                                    FROM PARSING_DSF
                                    WHERE TaskName = curTaskName);

            -- 평가 개수 계산
            SELECT COUNT(*) INTO varEvaluationNum
            FROM EVALUATION
            WHERE FK_idEstimator = varFK_idEstimator
            AND Status = 'done'
            AND FK_idPARSING_DSF IN (SELECT idPARSING_DSF
                                    FROM PARSING_DSF
                                    WHERE TaskName = curTaskName);

            SELECT AVG(Score) INTO varAvgScore
            FROM EVALUATION
            WHERE Status = 'done'
            AND FK_idPARSING_DSF IN (SELECT idPARSING_DSF
                                    FROM PARSING_DSF
                                    WHERE TaskName = curTaskName);

            SELECT STD(Score) INTO varSTDScore
            FROM EVALUATION
            WHERE Status = 'done'
            AND FK_idPARSING_DSF IN (SELECT idPARSING_DSF
                                    FROM PARSING_DSF
                                    WHERE TaskName = curTaskName);

            IF varAvgScore IS NULL THEN
                SET varAvgScore = 0;
            END IF;

            IF varSTDScore IS NULL THEN
                SET varSTDScore = 1;
            END IF;

            SET varSmallIndex = 0;
            SET varOutlierCount = 0;

            DROP TEMPORARY TABLE IF EXISTS NormZtable;

            CREATE TEMPORARY TABLE  IF NOT EXISTS NormZtable AS
                SELECT ABS((Score - varAvgScore)/varSTDScore) AS NormZ, ROW_NUMBER() OVER() AS IndexNum
                FROM EVALUATION
                WHERE FK_idEstimator = varFK_idEstimator
                AND Status = 'done'
                AND FK_idPARSING_DSF IN (SELECT idPARSING_DSF
                                FROM PARSING_DSF
                                WHERE TaskName = curTaskName)
                AND Score IS NOT NULL;

            smallloop: LOOP
                SET varSmallIndex = varSmallIndex + 1;
                SET varNormZ = NULL;

                SELECT NormZ INTO varNormZ
                FROM NormZtable
                WHERE IndexNum=varSmallIndex;

                IF varNormZ > 1 THEN
                    SET varOutlierCount = varOutlierCount + 1;
                END IF;

                IF varSmallIndex = varEvaluationNum THEN
                    LEAVE smallloop;
                END IF;
            END LOOP smallloop;


            SELECT COUNT(*) INTO varGoodEvaluationNum
            FROM EVALUATION AS E
            WHERE E.FK_idEstimator = varFK_idEstimator
                AND Status = 'done'
                AND E.Pass = (SELECT P.Pass
                            FROM PARSING_DSF AS P
                            WHERE P.idPARSING_DSF = E.FK_idPARSING_DSF
                            AND P.TotalStatus = 'done')
                AND E.FK_idPARSING_DSF IN (SELECT idPARSING_DSF
                                    FROM PARSING_DSF
                                    WHERE TaskName = curTaskName);

            SET newEstimatorScore = 40*varEvaluationNum/varFileNum
                                    + 30*(1-(varOutlierCount/varEvaluationNum))
                                    + 30*varGoodEvaluationNum/varEvaluationNum;

            SELECT UserScore INTO currUserScore
            FROM USER
            WHERE idUSER = varFK_idEstimator;

            UPDATE USER
                SET UserScore = 0.85*currUserScore + 0.15*newEstimatorScore
                WHERE idUSER = varFK_idEstimator;

            IF varIndex = varEstimatorNum THEN
                LEAVE myloop;
            END IF;
        END LOOP myloop;
    END IF;
END;

