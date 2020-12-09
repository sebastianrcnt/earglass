create definer = team9@`%` trigger AfterTaskDoneUpdateSubmitterScore
    after update
    on TASK
    for each row
BEGIN
    DECLARE varPassNum Int(11);
    DECLARE curTaskName varchar(40);
    DECLARE varIndex Int(11);
    DECLARE varSubmitterNum Int(11);
    DECLARE varSubmitterID Int(11);
    DECLARE varSubmitNum Int(11);
    DECLARE varMaxTotalScore Float;
    DECLARE varAvgTotalScore Float;
    DECLARE varSubmitNumRatio Float;
    DECLARE newSubmitterScore Float;
    DECLARE currUserScore Float;

    SET curTaskName = NEW.TaskName;
    SET varIndex = 0;

    IF (NEW.Status = 'done') THEN

        SELECT COUNT(*)
        INtO varSubmitterNum
        FROM SubmittersInDoneTask
        WHERE TaskName = curTaskName;

        myloop:
        LOOP
            SET varIndex = varIndex + 1;
            IF varSubmitNum = 0 THEN
                LEAVE myloop;
            end if;
            SELECT SubmitterID
            INTO varSubmitterID
            FROM SubmittersInDoneTask
            WHERE TaskName = curTaskName
              AND IndexNum = varIndex;

            -- pass 수 계산
            SELECT COUNT(*)
            INTO varPassNum
            FROM PARSING_DSF
            WHERE TaskName = curTaskName
              AND SubmitterID = varSubmitterID
              AND Pass = 'P'
            AND TotalStatus = 'done';

            SELECT IFNULL(MAX(SubmitNum),0)
            INTO varSubmitNum
            FROM PARSING_DSF
            WHERE TaskName = curTaskName
              AND SubmitterID = varSubmitterID
              AND SubmitNum IS NOT NULL;

            -- total score 평균 계산
            SELECT IFNULL(MAX(TotalScore),0)
            INTO varMaxTotalScore
            FROM PARSING_DSF
            WHERE TaskName = curTaskName
              AND TotalStatus = 'done'
            AND TotalScore IS NOT NULL;

            SELECT IFNULL(AVG(TotalScore),0)
            INTO varAvgTotalScore
            FROM PARSING_DSF
            WHERE TaskName = curTaskName
              AND SubmitterID = varSubmitterID
              AND TotalStatus = 'done'
            AND TotalScore IS NOT NULL;

            -- 제출 수 비율
            IF varSubmitNum > 100 THEN
                SET varSubmitNumRatio = 1;
            ELSE
                SET varSubmitNumRatio = (900 + varSubmitNum) / 1000;
            END IF;

            IF varSubmitNum = 0 THEN
                SET varSubmitNum = 1;
                SET varPassNum = 0;
            end if;

            IF varMaxTotalScore = 0 THEN
                SET varMaxTotalScore = 1;
                SET varAvgTotalScore = 0;
            end if;

            SET newSubmitterScore = (varPassNum / varSubmitNum) * 40
                + 50 * (varAvgTotalScore / varMaxTotalScore)
                + 10 * varSubmitNumRatio;

            SELECT UserScore
            INTO currUserScore
            FROM USER
            WHERE idUSER = varSubmitterID;

            UPDATE USER
            SET UserScore = 0.85 * currUserScore + 0.15 * newSubmitterScore
            WHERE idUSER = varSubmitterID;

            IF varIndex = varSubmitterNum THEN
                LEAVE myloop;
            END IF;
        END LOOP myloop;
    END IF;
END;

