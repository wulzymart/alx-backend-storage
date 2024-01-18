-- creates a stored procedure that computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
	UPDATE users SET average_score = (
		SELECT SUM(score * weight) / SUM(weight)
		FROM corrections
		LEFT JOIN projects ON corrections.project_id = projects.id
		WHERE user_id = userid
	) WHERE id = userid;
END; $$
DELIMITER ;