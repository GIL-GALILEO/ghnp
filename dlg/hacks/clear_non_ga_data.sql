SET FOREIGN_KEY_CHECKS = 0;
DELETE FROM chronam.core_awardee WHERE org_code != 'dlg';
DELETE FROM chronam.core_institution WHERE STATE != 'GA';
SET FOREIGN_KEY_CHECKS = 1;