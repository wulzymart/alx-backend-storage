-- computes and store the average score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
    DECLARE total_score INT DEFAULT 0;
    DECLARE total_projects INT DEFAULT 0;

    SELECT SUM(score)
        INTO total_score
        FROM corrections
        WHERE corrections.user_id = user_id;
    SELECT COUNT(*)
        INTO total_projects
        FROM corrections
        WHERE corrections.user_id = user_id;

    UPDATE users
        SET users.average_score = IF(projects_count = 0, 0, total_score / total_projects)
        WHERE users.id = user_id;
END $$
DELIMITER ;