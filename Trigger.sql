USE PC;
GO
CREATE TRIGGER trg_StatusUpdate
ON basic_info
AFTER INSERT, UPDATE
AS
BEGIN
    DECLARE @ip VARCHAR(15)
    DECLARE @last_status BIT
    DECLARE @data_status DATETIME

    SELECT @ip = inserted.ip, @last_status = inserted.last_status, @data_status = inserted.data_status
    FROM inserted

    INSERT INTO statuses (basic_info_id, status_, status_date)
    SELECT id, @last_status, @data_status
    FROM basic_info
    WHERE ip = @ip
END

Go