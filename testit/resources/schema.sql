-- *************** SqlDBM: PostgreSQL ****************;
-- ***************************************************;

DROP TABLE IF EXISTS s_cim_role;


DROP TABLE IF EXISTS s_cim_reinsurance_contract;


DROP TABLE IF EXISTS s_cim_product;


DROP TABLE IF EXISTS s_cim_policy_layer;


DROP TABLE IF EXISTS s_cim_policy;


DROP TABLE IF EXISTS s_cim_natural_party;


DROP TABLE IF EXISTS s_cim_loss_event;


DROP TABLE IF EXISTS s_cim_location;


DROP TABLE IF EXISTS s_cim_legal_party;


DROP TABLE IF EXISTS s_cim_insured_object;


DROP TABLE IF EXISTS s_cim_event;


DROP TABLE IF EXISTS s_cim_coverage_group;


DROP TABLE IF EXISTS s_cim_coverage_detail;


DROP TABLE IF EXISTS s_cim_coverage;


DROP TABLE IF EXISTS s_cim_claim;


DROP TABLE IF EXISTS l_program_policy;


DROP TABLE IF EXISTS l_product_policy;


DROP TABLE IF EXISTS l_portfolio_policy;


DROP TABLE IF EXISTS l_policy_reinsurance_contract;


DROP TABLE IF EXISTS l_policy_layer_reinsurance_contract;


DROP TABLE IF EXISTS l_policy_layer_policy_group;


DROP TABLE IF EXISTS l_policy_coverage_group;


DROP TABLE IF EXISTS l_policy_claim;


DROP TABLE IF EXISTS l_party_policy;


DROP TABLE IF EXISTS l_location_party;


DROP TABLE IF EXISTS l_location_insured_object;


DROP TABLE IF EXISTS l_insured_object_coverage;


DROP TABLE IF EXISTS l_insured_object_claim;


DROP TABLE IF EXISTS l_event_loss_event;


DROP TABLE IF EXISTS l_event_claim;


DROP TABLE IF EXISTS l_coverage_policy;


DROP TABLE IF EXISTS l_coverage_group_coverage;


DROP TABLE IF EXISTS l_claim_location;


DROP TABLE IF EXISTS h_role;


DROP TABLE IF EXISTS h_reinsurance_contract;


DROP TABLE IF EXISTS h_program;


DROP TABLE IF EXISTS h_product;


DROP TABLE IF EXISTS h_portfolio;


DROP TABLE IF EXISTS h_policy_layer;


DROP TABLE IF EXISTS h_policy;


DROP TABLE IF EXISTS h_party;


DROP TABLE IF EXISTS h_loss_event;


DROP TABLE IF EXISTS h_location;


DROP TABLE IF EXISTS h_insured_object;


DROP TABLE IF EXISTS h_event;


DROP TABLE IF EXISTS h_coverage_group;


DROP TABLE IF EXISTS h_coverage;


DROP TABLE IF EXISTS h_claim;



-- ************************************** h_role

CREATE TABLE IF NOT EXISTS h_role
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_party_copy PRIMARY KEY ( bk )
);

COMMENT ON TABLE h_role IS 'HUB for Allianz Organization Entity';

COMMENT ON COLUMN h_role.bk IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(party_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN h_role.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_role.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_role.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_role.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_role.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_reinsurance_contract

CREATE TABLE IF NOT EXISTS h_reinsurance_contract
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_policy_copy_1 PRIMARY KEY ( bk )
);



COMMENT ON COLUMN h_reinsurance_contract.bk IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(local_policy_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN h_reinsurance_contract.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_reinsurance_contract.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_reinsurance_contract.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_reinsurance_contract.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_reinsurance_contract.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_program

CREATE TABLE IF NOT EXISTS h_program
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_program PRIMARY KEY ( bk )
);

COMMENT ON TABLE h_program IS 'HUB for Allianz Organization Entity';

COMMENT ON COLUMN h_program.bk IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(local_program_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN h_program.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN h_program.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_program.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_program.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_program.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';





-- ************************************** h_product

CREATE TABLE IF NOT EXISTS h_product
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_policy_term_copy PRIMARY KEY ( bk )
);



COMMENT ON COLUMN h_product.bk IS 'Hashvalue generated from business keys ~ OE_ID ~ Source_SYSTEM_ID (local_policy_id~oe_id~source_system_id)';
COMMENT ON COLUMN h_product.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_product.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_product.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_product.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_product.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_portfolio

CREATE TABLE IF NOT EXISTS h_portfolio
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_policy_copy_3 PRIMARY KEY ( bk )
);



COMMENT ON COLUMN h_portfolio.bk IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(local_policy_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN h_portfolio.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_portfolio.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_portfolio.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_portfolio.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_portfolio.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_policy_layer

CREATE TABLE IF NOT EXISTS h_policy_layer
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_policy_copy_2 PRIMARY KEY ( bk )
);



COMMENT ON COLUMN h_policy_layer.bk IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(local_policy_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN h_policy_layer.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_policy_layer.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_policy_layer.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_policy_layer.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_policy_layer.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_policy

CREATE TABLE IF NOT EXISTS h_policy
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_policy PRIMARY KEY ( bk )
);



COMMENT ON COLUMN h_policy.bk IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(local_policy_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN h_policy.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_policy.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_policy.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_policy.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_policy.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_party

CREATE TABLE IF NOT EXISTS h_party
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_party PRIMARY KEY ( bk )
);

COMMENT ON TABLE h_party IS 'HUB for Allianz Organization Entity';

COMMENT ON COLUMN h_party.bk IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(party_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN h_party.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_party.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_party.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_party.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_party.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_loss_event

CREATE TABLE IF NOT EXISTS h_loss_event
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_claim_copy_copy PRIMARY KEY ( bk )
);



COMMENT ON COLUMN h_loss_event.bk IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(local_claim_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN h_loss_event.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_loss_event.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_loss_event.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_loss_event.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_loss_event.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_location

CREATE TABLE IF NOT EXISTS h_location
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_address PRIMARY KEY ( bk )
);

COMMENT ON TABLE h_location IS 'HUB for Allianz Organization Entity';

COMMENT ON COLUMN h_location.bk IS 'Business key (BK): concatination of the fields local_policy_id and inception_date (local_policy_id ||"_"|| inception_date)';
COMMENT ON COLUMN h_location.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_location.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_location.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_location.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_location.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_insured_object

CREATE TABLE IF NOT EXISTS h_insured_object
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_insurable_object PRIMARY KEY ( bk )
);

COMMENT ON TABLE h_insured_object IS 'HUB for Allianz Organization Entity';

COMMENT ON COLUMN h_insured_object.bk IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(Insured_object_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN h_insured_object.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_insured_object.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_insured_object.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_insured_object.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_insured_object.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_event

CREATE TABLE IF NOT EXISTS h_event
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_claim_copy PRIMARY KEY ( bk )
);



COMMENT ON COLUMN h_event.bk IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(local_claim_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN h_event.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_event.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_event.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_event.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_event.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_coverage_group

CREATE TABLE IF NOT EXISTS h_coverage_group
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_policy_term_copy_1 PRIMARY KEY ( bk )
);



COMMENT ON COLUMN h_coverage_group.bk IS 'Hashvalue generated from business keys ~ OE_ID ~ Source_SYSTEM_ID (local_policy_id~oe_id~source_system_id)';
COMMENT ON COLUMN h_coverage_group.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_coverage_group.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_coverage_group.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_coverage_group.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_coverage_group.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_coverage

CREATE TABLE IF NOT EXISTS h_coverage
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_policy_term PRIMARY KEY ( bk )
);



COMMENT ON COLUMN h_coverage.bk IS 'Hashvalue generated from business keys ~ OE_ID ~ Source_SYSTEM_ID (local_policy_id~oe_id~source_system_id)';
COMMENT ON COLUMN h_coverage.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_coverage.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_coverage.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_coverage.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_coverage.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** h_claim

CREATE TABLE IF NOT EXISTS h_claim
(
 bk               varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_h_claim PRIMARY KEY ( bk )
);



COMMENT ON COLUMN h_claim.bk IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(local_claim_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN h_claim.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN h_claim.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN h_claim.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN h_claim.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN h_claim.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** s_cim_role

CREATE TABLE IF NOT EXISTS s_cim_role
(
 bk                       varchar NOT NULL,
 cim_load_from_ts         timestamp NOT NULL,
 biz_eff_from_ts          timestamp NOT NULL,
 cim_load_to_ts           timestamp NOT NULL,
 cim_last_modification_ts timestamp NOT NULL,
 cim_invalid_ts           timestamp NULL,
 cim_src_sys_id           integer NOT NULL,
 cim_oe_id                integer NOT NULL,
 lc_role_cd               integer NOT NULL,
 role_name                varchar NOT NULL,
 CONSTRAINT s_cim_role PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);

COMMENT ON TABLE s_cim_role IS 'Satellite includes role reference information.';

COMMENT ON COLUMN s_cim_role.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN s_cim_role.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_role.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_role.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_role.bk IS 'Business key for identifying a role uniquely.';
COMMENT ON COLUMN s_cim_role.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_role.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_role.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';





-- ************************************** s_cim_reinsurance_contract

CREATE TABLE IF NOT EXISTS s_cim_reinsurance_contract
(
 bk                              varchar NOT NULL,
 cim_load_from_ts                timestamp NOT NULL,
 biz_eff_from_ts                 timestamp NOT NULL,
 cim_load_to_ts                  timestamp NOT NULL,
 cim_last_modification_ts        timestamp NOT NULL,
 cim_invalid_ts                  timestamp NULL,
 cim_src_sys_id                  integer NOT NULL,
 cim_oe_id                       integer NOT NULL,
 reinsurance_contract_identifier varchar NULL,
 reinsurance_inception_date      date NULL,
 reinsurance_expiry_date         date NULL,
 reinsurance_product             varchar NULL,
 inuring_priority                numeric NULL,
 external_ri                     numeric NULL,
 lc_reinsurance_currency_cd      varchar NULL,
 reinsurance_attachment_point    numeric NULL,
 reinsurance_limit               numeric NULL,
 share_ceded                     numeric NULL,
 allianz_group_share_from_ceded  numeric NULL,
 CONSTRAINT PK_s_midcorp_policy_term_copy_clone PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);



COMMENT ON COLUMN s_cim_reinsurance_contract.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_reinsurance_contract.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_reinsurance_contract.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_reinsurance_contract.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_reinsurance_contract.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_reinsurance_contract.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_reinsurance_contract.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN s_cim_reinsurance_contract.reinsurance_inception_date IS 'The inception date of the policy whose exposure information is displayed.
• This represents the date the coverage of the policy starts for this coverage period.
• In case [INCEPTION_DATE] is unknown, the reported policy is considered to be effective.
• In general, this date is different to the date the policy was underwritten the first time, unless it is a new business';
COMMENT ON COLUMN s_cim_reinsurance_contract.reinsurance_expiry_date IS 'Expiry date of the policy whose exposure information is displayed.
• This represents the date the coverage of the policy ends.';
COMMENT ON COLUMN s_cim_reinsurance_contract.bk IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';





-- ************************************** s_cim_product

CREATE TABLE IF NOT EXISTS s_cim_product
(
 bk                       varchar NOT NULL,
 cim_load_from_ts         timestamp NOT NULL,
 biz_eff_from_ts          timestamp NOT NULL,
 cim_load_to_ts           timestamp NOT NULL,
 cim_last_modification_ts timestamp NOT NULL,
 cim_invalid_ts           timestamp NULL,
 cim_src_sys_id           integer NOT NULL,
 cim_oe_id                integer NOT NULL,
 product_identifier       numeric NULL,
 lc_product_cd            varchar NULL,
 product_name             varchar NOT NULL,
 CONSTRAINT PK_s_cim_reinsurance_clone_copy PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);

COMMENT ON TABLE s_cim_product IS 'Satellite';

COMMENT ON COLUMN s_cim_product.bk IS 'Business key for identifying a role uniquely.';
COMMENT ON COLUMN s_cim_product.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_product.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_product.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_product.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_product.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_product.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_product.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** s_cim_policy_layer

CREATE TABLE IF NOT EXISTS s_cim_policy_layer
(
 bk                            varchar NOT NULL,
 cim_load_from_ts              timestamp NOT NULL,
 biz_eff_from_ts               timestamp NOT NULL,
 cim_load_to_ts                timestamp NOT NULL,
 cim_last_modification_ts      timestamp NOT NULL,
 cim_invalid_ts                timestamp NULL,
 cim_src_sys_id                integer NOT NULL,
 cim_oe_id                     integer NOT NULL,
 policy_layer_identifier       varchar NULL,
 layer_name                    varchar NULL,
 layer_number                  numeric NULL,
 layer_attachment_point_amount numeric NULL,
 layer_limit_amount            numeric NULL,
 layer_currency_cd             varchar NULL,
 primary_layer_flag            varchar NULL,
 CONSTRAINT PK_s_midcorp_claim_copy PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);



COMMENT ON COLUMN s_cim_policy_layer.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_policy_layer.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN s_cim_policy_layer.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_policy_layer.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_policy_layer.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_policy_layer.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_policy_layer.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';





-- ************************************** s_cim_policy

CREATE TABLE IF NOT EXISTS s_cim_policy
(
 bk                            varchar NOT NULL,
 cim_load_from_ts              timestamp NOT NULL,
 biz_eff_from_ts               timestamp NOT NULL,
 cim_load_to_ts                timestamp NOT NULL,
 cim_last_modification_ts      timestamp NOT NULL,
 cim_invalid_ts                timestamp NULL,
 cim_src_sys_id                integer NOT NULL,
 cim_oe_id                     integer NOT NULL,
 policy_identifier             varchar NULL,
 policy_number                 varchar NULL,
 inception_date                date NULL,
 expiry_date                   date NULL,
 lta_flag                      numeric NULL,
 original_underwriting_date    date NULL,
 lc_policy_status_cd           varchar NULL,
 cancellation_date             date NULL,
 lc_cancellation_reason_cd     varchar NULL,
 lc_business_role_cd           varchar NULL,
 lc_applicable_jurisdiction_cd varchar NULL,
 primary_excess_liability_flag varchar NULL,
 lc_territorial_coverage_cd    varchar NULL,
 lc_portfolio_cd               varchar NULL,
 lc_classification_cd          varchar NULL,
 lc_sub_classification_cd      varchar NULL,
 lc_customer_segment_cd        varchar NULL,
 lc_business_type_cd           varchar NULL,
 lc_assumed_business_type_cd   varchar NULL,
 lc_business_activity_cd       varchar NULL,
 lc_s2_line_of_business_cd     varchar NULL,
 facultative_cession_flag      numeric NULL,
 lc_coverage_trigger_cd        varchar NULL,
 lc_sales_channel_cd           varchar NULL,
 lc_policy_currency_cd         varchar NULL,
 commission_share              numeric NULL,
 utility_extension_flag        varchar NULL,
 insurers_gross_policy_share   numeric NULL,
 CONSTRAINT PK_s_midcorp_policy_copy PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);



COMMENT ON COLUMN s_cim_policy.policy_identifier IS 'Original policy identifier as used in the OE, necessary to be able to refer to local systems.  In case of multi-underwriting-period, multi-insurance-cover or multi-layer policies in local systems, the local policy needs to be split in different GIRDA policy ID';
COMMENT ON COLUMN s_cim_policy.original_underwriting_date IS 'The date when the policy was underwritten for the first time (i.e. equal to inception date only for new business)';
COMMENT ON COLUMN s_cim_policy.inception_date IS 'The inception date of the policy whose exposure information is displayed.
• This represents the date the coverage of the policy starts for this coverage period.
• In case [INCEPTION_DATE] is unknown, the reported policy is considered to be effective.
• In general, this date is different to the date the policy was underwritten the first time, unless it is a new business';
COMMENT ON COLUMN s_cim_policy.expiry_date IS 'Expiry date of the policy whose exposure information is displayed.
• This represents the date the coverage of the policy ends.';
COMMENT ON COLUMN s_cim_policy.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_policy.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_policy.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_policy.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_policy.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_policy.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_policy.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** s_cim_natural_party

CREATE TABLE IF NOT EXISTS s_cim_natural_party
(
 bk                       varchar NOT NULL,
 cim_load_from_ts         timestamp NOT NULL,
 biz_eff_from_ts          timestamp NOT NULL,
 cim_load_to_ts           timestamp NOT NULL,
 cim_last_modification_ts timestamp NOT NULL,
 cim_invalid_ts           timestamp NULL,
 cim_src_sys_id           integer NOT NULL,
 cim_oe_id                integer NOT NULL,
 party_identifier         varchar NULL,
 party_name               varchar NULL,
 date_of_birth            date NULL,
 lc_gender_cd             varchar NULL,
 lc_occupation_cd         varchar NULL,
 CONSTRAINT PK_s_cim_natural_party PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);

COMMENT ON TABLE s_cim_natural_party IS 'Table including information about natural parties.';

COMMENT ON COLUMN s_cim_natural_party.bk IS 'Business key for identifying a party uniquely.';
COMMENT ON COLUMN s_cim_natural_party.party_identifier IS 'Unique identifier of a natural party.';
COMMENT ON COLUMN s_cim_natural_party.party_name IS 'Name of the natural party.';
COMMENT ON COLUMN s_cim_natural_party.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_natural_party.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_natural_party.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_natural_party.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_natural_party.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_natural_party.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_natural_party.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN s_cim_natural_party.date_of_birth IS 'Insured person date of birth is the specific date, month & year the insured person was born on.';
COMMENT ON COLUMN s_cim_natural_party.lc_gender_cd IS 'Gender of the insured person.';
COMMENT ON COLUMN s_cim_natural_party.lc_occupation_cd IS 'Occupation of the insured person';





-- ************************************** s_cim_loss_event

CREATE TABLE IF NOT EXISTS s_cim_loss_event
(
 bk                       varchar NOT NULL,
 cim_load_from_ts         timestamp NOT NULL,
 biz_eff_from_ts          timestamp NOT NULL,
 cim_load_to_ts           timestamp NOT NULL,
 cim_last_modification_ts timestamp NOT NULL,
 cim_invalid_ts           timestamp NULL,
 cim_src_sys_id           integer NOT NULL,
 cim_oe_id                integer NOT NULL,
 loss_event_identifier    varchar NOT NULL,
 catastrophe_flag         numeric NULL,
 CONSTRAINT PK_s_cim_location_copy_copy PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);

COMMENT ON TABLE s_cim_loss_event IS 'Satellite including location information.';

COMMENT ON COLUMN s_cim_loss_event.bk IS 'Business key for uniquely identifying a location.';
COMMENT ON COLUMN s_cim_loss_event.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_loss_event.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_loss_event.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_loss_event.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_loss_event.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_loss_event.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_loss_event.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN s_cim_loss_event.loss_event_identifier IS 'Unique identifier of a loaction.';





-- ************************************** s_cim_location

CREATE TABLE IF NOT EXISTS s_cim_location
(
 bk                       varchar NOT NULL,
 cim_load_from_ts         timestamp NOT NULL,
 biz_eff_from_ts          timestamp NOT NULL,
 cim_load_to_ts           timestamp NOT NULL,
 cim_last_modification_ts timestamp NOT NULL,
 cim_invalid_ts           timestamp NULL,
 cim_src_sys_id           integer NOT NULL,
 cim_oe_id                integer NOT NULL,
 location_identifier      varchar NOT NULL,
 lc_country_cd            varchar NULL,
 region                   varchar NULL,
 sub_region               varchar NULL,
 postcode                 varchar NULL,
 city                     varchar NULL,
 street_name              varchar NULL,
 house_number             varchar NULL,
 CONSTRAINT PK_s_cim_location PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);

COMMENT ON TABLE s_cim_location IS 'Satellite including location information.';

COMMENT ON COLUMN s_cim_location.bk IS 'Business key for uniquely identifying a location.';
COMMENT ON COLUMN s_cim_location.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_location.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_location.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_location.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_location.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_location.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_location.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN s_cim_location.location_identifier IS 'Unique identifier of a loaction.';





-- ************************************** s_cim_legal_party

CREATE TABLE IF NOT EXISTS s_cim_legal_party
(
 bk                                 varchar NOT NULL,
 cim_load_from_ts                   timestamp NOT NULL,
 biz_eff_from_ts                    timestamp NOT NULL,
 cim_load_to_ts                     timestamp NOT NULL,
 cim_last_modification_ts           timestamp NOT NULL,
 cim_invalid_ts                     timestamp NULL,
 cim_src_sys_id                     integer NOT NULL,
 cim_oe_id                          integer NOT NULL,
 party_identifier                   varchar NULL,
 party_name                         varchar NULL,
 local_legal_id                     varchar NULL,
 lc_legal_id_provider_cd            varchar NULL,
 party_lei_id                       varchar NULL,
 euler_hermes_id                    varchar NULL,
 party_ultimate_parent_company_name varchar NULL,
 lc_turnover_currency_cd            varchar NULL,
 lc_broker_segmentation_cd          varchar NULL,
 policyholder_turnover              numeric NULL,
 employees_number                   integer NULL,
 CONSTRAINT PK_s_cim_legal_party_copy PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);

COMMENT ON TABLE s_cim_legal_party IS 'Table including information regarding legal party.';

COMMENT ON COLUMN s_cim_legal_party.party_lei_id IS 'Legal Entity Identifier of the Policyholder (only for non retail business).';
COMMENT ON COLUMN s_cim_legal_party.euler_hermes_id IS 'Euler Hermes Identifier of the Policyholder.';
COMMENT ON COLUMN s_cim_legal_party.bk IS 'Business key for identifying a role uniquely.';
COMMENT ON COLUMN s_cim_legal_party.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_legal_party.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-31 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_legal_party.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_legal_party.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_legal_party.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_legal_party.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_legal_party.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN s_cim_legal_party.lc_broker_segmentation_cd IS 'Legal Entity Identifier of the Policyholder (only for non retail business).';





-- ************************************** s_cim_insured_object

CREATE TABLE IF NOT EXISTS s_cim_insured_object
(
 bk                            varchar NOT NULL,
 cim_load_from_ts              timestamp NOT NULL,
 biz_eff_from_ts               timestamp NOT NULL,
 cim_load_to_ts                timestamp NOT NULL,
 cim_last_modification_ts      timestamp NOT NULL,
 cim_invalid_ts                timestamp NULL,
 cim_src_sys_id                integer NOT NULL,
 cim_oe_id                     integer NOT NULL,
 insured_object_identifier     varchar NULL,
 lc_insured_object_type_cd     varchar NULL,
 lc_business_activity_cd       varchar NULL,
 lc_az_isic_plus_cd            varchar NULL,
 lc_surveyed_lce_cd            varchar NULL,
 grouped_location_flag         varchar NULL,
 lc_insured_object_currency_cd varchar NULL,
 insured_object_sum_insured    numeric NULL,
 builidng_sum_insured          numeric NULL,
 contents_sum_insured          numeric NULL,
 sum_insured_bi                numeric NULL,
 lc_territorial_coverage_cd    varchar NULL,
 lc_exposure_base_cd           numeric NULL,
 liability_exposure_amount     numeric NULL,
 CONSTRAINT PK_s_midcorp_insurable_object PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);



COMMENT ON COLUMN s_cim_insured_object.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_insured_object.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_insured_object.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_insured_object.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_insured_object.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_insured_object.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_insured_object.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** s_cim_event

CREATE TABLE IF NOT EXISTS s_cim_event
(
 bk                       varchar NOT NULL,
 cim_load_from_ts         timestamp NOT NULL,
 biz_eff_from_ts          timestamp NOT NULL,
 cim_load_to_ts           timestamp NOT NULL,
 cim_last_modification_ts timestamp NOT NULL,
 cim_invalid_ts           timestamp NULL,
 cim_src_sys_id           integer NOT NULL,
 cim_oe_id                integer NOT NULL,
 event_identifier         varchar NOT NULL,
 event_name               varchar NULL,
 event_cause              varchar NULL,
 event_desc               varchar NULL,
 lc_event_status_cd       varchar NULL,
 event_date_from          date NULL,
 event_date_to            date NULL,
 CONSTRAINT PK_s_cim_location_copy PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);

COMMENT ON TABLE s_cim_event IS 'Satellite including location information.';

COMMENT ON COLUMN s_cim_event.bk IS 'Business key for uniquely identifying a location.';
COMMENT ON COLUMN s_cim_event.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_event.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_event.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_event.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_event.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_event.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_event.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN s_cim_event.event_identifier IS 'Unique identifier of a loaction.';





-- ************************************** s_cim_coverage_group

CREATE TABLE IF NOT EXISTS s_cim_coverage_group
(
 bk                            varchar NOT NULL,
 cim_load_from_ts              timestamp NOT NULL,
 biz_eff_from_ts               timestamp NOT NULL,
 cim_load_to_ts                timestamp NOT NULL,
 cim_last_modification_ts      timestamp NOT NULL,
 cim_invalid_ts                timestamp NULL,
 cim_src_sys_id                integer NOT NULL,
 cim_oe_id                     integer NOT NULL,
 coverage_group_identifier     varchar NULL,
 lc_line_of_business_cd        varchar NULL,
 lc_sub_line_of_business_cd    varchar NULL,
 lc_az_isic_plus_cd            varchar NULL,
 lc_coverage_group_currency_cd varchar NULL,
 portfolio_premium             numeric NULL,
 gross_written_premium         numeric NULL,
 gross_earned_premium          numeric NULL,
 fire_brigade_fees_levies      numeric NULL,
 premium_taxes                 numeric NULL,
 technical_price               numeric NULL,
 sum_insured                   numeric NULL,
 pml                           numeric NULL,
 eml                           numeric NULL,
 CONSTRAINT PK_s_midcorp_policy_copy_copy PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);



COMMENT ON COLUMN s_cim_coverage_group.coverage_group_identifier IS 'Original policy identifier as used in the OE, necessary to be able to refer to local systems.  In case of multi-underwriting-period, multi-insurance-cover or multi-layer policies in local systems, the local policy needs to be split in different GIRDA policy ID';
COMMENT ON COLUMN s_cim_coverage_group.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_coverage_group.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_coverage_group.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_coverage_group.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_coverage_group.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_coverage_group.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_coverage_group.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN s_cim_coverage_group.lc_az_isic_plus_cd IS 'Allianz Global Industrial activity code of the Policy or the main activity code of the largest location if the information is not available on Policy level
No local specific ISIC code should be provided.';





-- ************************************** s_cim_coverage_detail

CREATE TABLE IF NOT EXISTS s_cim_coverage_detail
(
 bk                       varchar NOT NULL,
 cim_load_from_ts         timestamp NOT NULL,
 biz_eff_from_ts          timestamp NOT NULL,
 cim_load_to_ts           timestamp NOT NULL,
 cim_last_modification_ts timestamp NOT NULL,
 cim_invalid_ts           timestamp NULL,
 cim_src_sys_id           integer NOT NULL,
 cim_oe_id                integer NOT NULL,
 coverage_identifier      varchar NULL,
 deductible               numeric NULL,
 lc_deductible_logic_cd   varchar NULL,
 lc_deductible_scope_cd   varchar NULL,
 minimum_deductible       numeric NULL,
 aag                      numeric NULL,
 excess                   numeric NULL,
 bi_waiting_period        numeric NULL,
 bi_period_of_indemnity    NULL,
 limit_amount             numeric NULL,
 aal                      numeric NULL,
 lc_limit_scope_cd        varchar NULL,
 lc_coverage_currency_cd  varchar NULL,
 CONSTRAINT PK_s_cim_reinsurance_clone_1 PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);

COMMENT ON TABLE s_cim_coverage_detail IS 'Satellite';

COMMENT ON COLUMN s_cim_coverage_detail.bk IS 'Business key for identifying a role uniquely.';
COMMENT ON COLUMN s_cim_coverage_detail.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_coverage_detail.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_coverage_detail.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_coverage_detail.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_coverage_detail.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_coverage_detail.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_coverage_detail.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** s_cim_coverage

CREATE TABLE IF NOT EXISTS s_cim_coverage
(
 bk                           varchar NOT NULL,
 cim_load_from_ts             timestamp NOT NULL,
 biz_eff_from_ts              timestamp NOT NULL,
 cim_load_to_ts               timestamp NOT NULL,
 cim_last_modification_ts     timestamp NOT NULL,
 cim_invalid_ts               timestamp NULL,
 cim_src_sys_id               integer NOT NULL,
 cim_oe_id                    integer NOT NULL,
 coverage_identifier          varchar NOT NULL,
 lc_perils_cd                 varchar NULL,
 lc_coverage_currency_cd      varchar NULL,
 lc_peril_specific_premium_cd numeric NULL,
 coverage_start_date          date NULL,
 coverage_end_date            date NULL,
 CONSTRAINT PK_s_midcorp_policy_term PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);



COMMENT ON COLUMN s_cim_coverage.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_coverage.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';
COMMENT ON COLUMN s_cim_coverage.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_coverage.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_coverage.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_coverage.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_coverage.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN s_cim_coverage.coverage_start_date IS 'The inception date of the policy whose exposure information is displayed.
• This represents the date the coverage of the policy starts for this coverage period.
• In case [INCEPTION_DATE] is unknown, the reported policy is considered to be effective.
• In general, this date is different to the date the policy was underwritten the first time, unless it is a new business';
COMMENT ON COLUMN s_cim_coverage.coverage_end_date IS 'Expiry date of the policy whose exposure information is displayed.
• This represents the date the coverage of the policy ends.';





-- ************************************** s_cim_claim

CREATE TABLE IF NOT EXISTS s_cim_claim
(
 bk                            varchar NOT NULL,
 cim_load_from_ts              timestamp NOT NULL,
 biz_eff_from_ts               timestamp NOT NULL,
 cim_load_to_ts                timestamp NOT NULL,
 cim_last_modification_ts      timestamp NOT NULL,
 cim_invalid_ts                timestamp NULL,
 cim_src_sys_id                integer NOT NULL,
 cim_oe_id                     integer NOT NULL,
 claim_identifier              varchar NULL,
 claim_number                  varchar NULL,
 lc_claim_status_cd            varchar NULL,
 lc_claim_type_cd              varchar NULL,
 lc_loss_cause_cd              varchar NULL,
 lc_line_of_business_cd        varchar NULL,
 lc_sub_line_of_business_cd    varchar NULL,
 claims_made_date              date NULL,
 loss_date                     date NULL,
 notification_date             date NULL,
 claim_cluster_code            varchar NULL,
 local_ll_flag                 numeric NULL,
 lc_claim_specific_cd          varchar NULL,
 lc_claim_currency_cd          varchar NULL,
 ground_up_loss                numeric NULL,
 paid_claim_amount_net_alae    numeric NULL,
 case_reserves_amount_net_alae numeric NULL,
 paid_alae_amount              numeric NULL,
 alae_reserves_amount          numeric NULL,
 CONSTRAINT PK_s_midcorp_claim PRIMARY KEY ( bk, cim_load_from_ts, biz_eff_from_ts )
);



COMMENT ON COLUMN s_cim_claim.alae_reserves_amount IS 'Case reserves for allocated loss adjustment expenses (ALAE) amounts, if these are recorded separately, consistent with the chart of accounts used for GAPC submission';
COMMENT ON COLUMN s_cim_claim.case_reserves_amount_net_alae IS 'Indemnity amounts recorded as case reserves, consistent with the chart of accounts used for GAPC submission';
COMMENT ON COLUMN s_cim_claim.ground_up_loss IS 'Ground up loss amount before application of policy/contract conditions and reinsurance. It is 100% of the reported loss by claimant. This amount is reported in claim currency.';
COMMENT ON COLUMN s_cim_claim.paid_alae_amount IS 'Allocated Loss Adjustment Expenses (ALAE) recorded as paid, if these are recorded separately, consistent with the chart of accounts used for GAPC submission';
COMMENT ON COLUMN s_cim_claim.paid_claim_amount_net_alae IS 'Indemnity amounts recorded as paid, cconsistent with the chart of accounts used for GAPC submissionn';
COMMENT ON COLUMN s_cim_claim.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN s_cim_claim.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN s_cim_claim.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN s_cim_claim.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN s_cim_claim.cim_last_modification_ts IS 'Timestamp of the last modification.';
COMMENT ON COLUMN s_cim_claim.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN s_cim_claim.biz_eff_from_ts IS 'Timestamp for business effectivity. If not available the default value ''9999-12-32 23:59:59'' should be provided.';





-- ************************************** l_program_policy

CREATE TABLE IF NOT EXISTS l_program_policy
(
 bk_policy        varchar NOT NULL,
 bk_program       varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_l_policy_program PRIMARY KEY ( bk_policy, bk_program )
);



COMMENT ON COLUMN l_program_policy.bk_policy IS 'Hashvalue generated from business keys of linked tables ~ OE_ID ~ Source_SYSTEM_ID';
COMMENT ON COLUMN l_program_policy.bk_program IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(local_program_id~gdp_oe_id~gdp_src_sys_id)';
COMMENT ON COLUMN l_program_policy.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_program_policy.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_program_policy.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_program_policy.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_program_policy.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_product_policy

CREATE TABLE IF NOT EXISTS l_product_policy
(
 bk_policy        varchar NOT NULL,
 bk_product       varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_l_policy_policy_term_copy PRIMARY KEY ( bk_policy, bk_product )
);

COMMENT ON TABLE l_product_policy IS 'peril_specific_premium
limit
limit_pd
limit_bi
deductible
deductible_pd
deductible_bi
bi_period_of_indemnity';

COMMENT ON COLUMN l_product_policy.bk_policy IS 'Hashvalue generated from business keys of linked tables ~ OE_ID~ Source_SYSTEM_ID';
COMMENT ON COLUMN l_product_policy.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_product_policy.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_product_policy.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_product_policy.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_product_policy.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_portfolio_policy

CREATE TABLE IF NOT EXISTS l_portfolio_policy
(
 bk_policy        varchar NOT NULL,
 bk_portfolio     varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_l_policy_claim_copy_1 PRIMARY KEY ( bk_policy, bk_portfolio )
);



COMMENT ON COLUMN l_portfolio_policy.bk_policy IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_portfolio_policy.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_portfolio_policy.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_portfolio_policy.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_portfolio_policy.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_portfolio_policy.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_policy_reinsurance_contract

CREATE TABLE IF NOT EXISTS l_policy_reinsurance_contract
(
 bk_reinsurance_contract varchar NOT NULL,
 bk_policy               varchar NOT NULL,
 cim_load_from_ts        timestamp NOT NULL,
 cim_load_to_ts          timestamp NOT NULL,
 cim_invalid_ts          timestamp NULL,
 cim_src_sys_id          integer NOT NULL,
 cim_oe_id               integer NOT NULL,
 CONSTRAINT PK_l_policy_reinsurance_contract PRIMARY KEY ( bk_reinsurance_contract, bk_policy )
);



COMMENT ON COLUMN l_policy_reinsurance_contract.bk_reinsurance_contract IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_policy_reinsurance_contract.bk_policy IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_policy_reinsurance_contract.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_policy_reinsurance_contract.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_policy_reinsurance_contract.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_policy_reinsurance_contract.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_policy_reinsurance_contract.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_policy_layer_reinsurance_contract

CREATE TABLE IF NOT EXISTS l_policy_layer_reinsurance_contract
(
 bk_reinsurance_contract varchar NOT NULL,
 bk_policy_layer         varchar NOT NULL,
 cim_load_from_ts        timestamp NOT NULL,
 cim_load_to_ts          timestamp NOT NULL,
 cim_invalid_ts          timestamp NULL,
 cim_src_sys_id          integer NOT NULL,
 cim_oe_id               integer NOT NULL,
 CONSTRAINT PK_l_policy_claim_copy_1_copy_copy PRIMARY KEY ( bk_reinsurance_contract, bk_policy_layer )
);



COMMENT ON COLUMN l_policy_layer_reinsurance_contract.bk_reinsurance_contract IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_policy_layer_reinsurance_contract.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_policy_layer_reinsurance_contract.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_policy_layer_reinsurance_contract.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_policy_layer_reinsurance_contract.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_policy_layer_reinsurance_contract.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_policy_layer_policy_group

CREATE TABLE IF NOT EXISTS l_policy_layer_policy_group
(
 bk_policy_layer   varchar NOT NULL,
 bk_coverage_group varchar NOT NULL,
 cim_load_from_ts  timestamp NOT NULL,
 cim_load_to_ts    timestamp NOT NULL,
 cim_invalid_ts    timestamp NULL,
 cim_src_sys_id    integer NOT NULL,
 cim_oe_id         integer NOT NULL,
 CONSTRAINT PK_l_policy_policy_term_copy_2 PRIMARY KEY ( bk_policy_layer, bk_coverage_group )
);

COMMENT ON TABLE l_policy_layer_policy_group IS 'peril_specific_premium
limit
limit_pd
limit_bi
deductible
deductible_pd
deductible_bi
bi_period_of_indemnity';

COMMENT ON COLUMN l_policy_layer_policy_group.bk_policy_layer IS 'Hashvalue generated from business keys of linked tables ~ OE_ID~ Source_SYSTEM_ID';
COMMENT ON COLUMN l_policy_layer_policy_group.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_policy_layer_policy_group.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_policy_layer_policy_group.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_policy_layer_policy_group.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_policy_layer_policy_group.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_policy_coverage_group

CREATE TABLE IF NOT EXISTS l_policy_coverage_group
(
 bk_policy         varchar NOT NULL,
 bk_coverage_group varchar NOT NULL,
 cim_load_from_ts  timestamp NOT NULL,
 cim_load_to_ts    timestamp NOT NULL,
 cim_invalid_ts    timestamp NULL,
 cim_src_sys_id    integer NOT NULL,
 cim_oe_id         integer NOT NULL,
 CONSTRAINT PK_l_policy_policy_term PRIMARY KEY ( bk_policy, bk_coverage_group )
);

COMMENT ON TABLE l_policy_coverage_group IS 'peril_specific_premium
limit
limit_pd
limit_bi
deductible
deductible_pd
deductible_bi
bi_period_of_indemnity';

COMMENT ON COLUMN l_policy_coverage_group.bk_policy IS 'Hashvalue generated from business keys of linked tables ~ OE_ID~ Source_SYSTEM_ID';
COMMENT ON COLUMN l_policy_coverage_group.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_policy_coverage_group.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_policy_coverage_group.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_policy_coverage_group.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_policy_coverage_group.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_policy_claim

CREATE TABLE IF NOT EXISTS l_policy_claim
(
 bk_policy        varchar NOT NULL,
 bk_claim         varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_l_policy_claim PRIMARY KEY ( bk_policy, bk_claim )
);



COMMENT ON COLUMN l_policy_claim.bk_policy IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_policy_claim.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_policy_claim.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_policy_claim.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_policy_claim.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_policy_claim.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_party_policy

CREATE TABLE IF NOT EXISTS l_party_policy
(
 bk_policy        varchar NOT NULL,
 bk_intermediary  varchar NOT NULL,
 bk_role          varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_l_policy_intermediary PRIMARY KEY ( bk_policy, bk_intermediary, bk_role )
);

COMMENT ON TABLE l_party_policy IS 'depending on the role filled in party file';

COMMENT ON COLUMN l_party_policy.bk_policy IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_party_policy.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_party_policy.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_party_policy.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_party_policy.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_party_policy.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';
COMMENT ON COLUMN l_party_policy.bk_role IS 'Hashvalue generated from business keys ~ OE_ID~ Source_SYSTEM_ID. HashValue(party_id~gdp_oe_id~gdp_src_sys_id)';





-- ************************************** l_location_party

CREATE TABLE IF NOT EXISTS l_location_party
(
 bk_party         varchar NOT NULL,
 bk_location      varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_l_party_address PRIMARY KEY ( bk_party, bk_location )
);



COMMENT ON COLUMN l_location_party.bk_party IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_location_party.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_location_party.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_location_party.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_location_party.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_location_party.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_location_insured_object

CREATE TABLE IF NOT EXISTS l_location_insured_object
(
 bk_insured_object varchar NOT NULL,
 bk_location       varchar NOT NULL,
 cim_load_from_ts  timestamp NOT NULL,
 cim_load_to_ts    timestamp NOT NULL,
 cim_invalid_ts    timestamp NULL,
 cim_src_sys_id    integer NOT NULL,
 cim_oe_id         integer NOT NULL,
 CONSTRAINT PK_l_insurable_object_address PRIMARY KEY ( bk_insured_object, bk_location )
);



COMMENT ON COLUMN l_location_insured_object.bk_location IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_location_insured_object.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_location_insured_object.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_location_insured_object.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_location_insured_object.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_location_insured_object.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_insured_object_coverage

CREATE TABLE IF NOT EXISTS l_insured_object_coverage
(
 bk_coverage       varchar NOT NULL,
 bk_insured_object varchar NOT NULL,
 cim_load_from_ts  timestamp NOT NULL,
 cim_load_to_ts    timestamp NOT NULL,
 cim_invalid_ts    timestamp NULL,
 cim_src_sys_id    integer NOT NULL,
 cim_oe_id         integer NOT NULL,
 CONSTRAINT PK_l_policy_insurable_object_copy_copy_1 PRIMARY KEY ( bk_coverage, bk_insured_object )
);



COMMENT ON COLUMN l_insured_object_coverage.bk_coverage IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_insured_object_coverage.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_insured_object_coverage.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_insured_object_coverage.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_insured_object_coverage.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_insured_object_coverage.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_insured_object_claim

CREATE TABLE IF NOT EXISTS l_insured_object_claim
(
 bk_claim          varchar NOT NULL,
 bk_insured_object varchar NOT NULL,
 cim_load_from_ts  timestamp NOT NULL,
 cim_load_to_ts    timestamp NOT NULL,
 cim_invalid_ts    timestamp NULL,
 cim_src_sys_id    integer NOT NULL,
 cim_oe_id         integer NOT NULL,
 CONSTRAINT PK_l_policy_insurable_object_copy_copy_copy_1 PRIMARY KEY ( bk_claim, bk_insured_object )
);



COMMENT ON COLUMN l_insured_object_claim.bk_claim IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_insured_object_claim.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_insured_object_claim.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_insured_object_claim.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_insured_object_claim.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_insured_object_claim.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_event_loss_event

CREATE TABLE IF NOT EXISTS l_event_loss_event
(
 bk_loss_event    varchar NOT NULL,
 bk_event         varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_l_policy_claim_copy_copy PRIMARY KEY ( bk_loss_event, bk_event )
);



COMMENT ON COLUMN l_event_loss_event.bk_loss_event IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_event_loss_event.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_event_loss_event.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_event_loss_event.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_event_loss_event.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_event_loss_event.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_event_claim

CREATE TABLE IF NOT EXISTS l_event_claim
(
 bk_event         varchar NOT NULL,
 bk_claim         varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_l_policy_claim_copy PRIMARY KEY ( bk_event, bk_claim )
);



COMMENT ON COLUMN l_event_claim.bk_event IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_event_claim.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_event_claim.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_event_claim.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_event_claim.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_event_claim.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_coverage_policy

CREATE TABLE IF NOT EXISTS l_coverage_policy
(
 bk_policy        varchar NOT NULL,
 bk_coverage      varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_l_policy_policy_term_copy_1 PRIMARY KEY ( bk_policy, bk_coverage )
);

COMMENT ON TABLE l_coverage_policy IS 'peril_specific_premium
limit
limit_pd
limit_bi
deductible
deductible_pd
deductible_bi
bi_period_of_indemnity';

COMMENT ON COLUMN l_coverage_policy.bk_policy IS 'Hashvalue generated from business keys of linked tables ~ OE_ID~ Source_SYSTEM_ID';
COMMENT ON COLUMN l_coverage_policy.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_coverage_policy.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_coverage_policy.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_coverage_policy.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_coverage_policy.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_coverage_group_coverage

CREATE TABLE IF NOT EXISTS l_coverage_group_coverage
(
 bk_coverage_group varchar NOT NULL,
 bk_coverage       varchar NOT NULL,
 cim_load_from_ts  timestamp NOT NULL,
 cim_load_to_ts    timestamp NOT NULL,
 cim_invalid_ts    timestamp NULL,
 cim_src_sys_id    integer NOT NULL,
 cim_oe_id         integer NOT NULL,
 CONSTRAINT PK_l_policy_policy_term_copy_1_copy PRIMARY KEY ( bk_coverage_group, bk_coverage )
);

COMMENT ON TABLE l_coverage_group_coverage IS 'peril_specific_premium
limit
limit_pd
limit_bi
deductible
deductible_pd
deductible_bi
bi_period_of_indemnity';

COMMENT ON COLUMN l_coverage_group_coverage.bk_coverage_group IS 'Hashvalue generated from business keys of linked tables ~ OE_ID~ Source_SYSTEM_ID';
COMMENT ON COLUMN l_coverage_group_coverage.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_coverage_group_coverage.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_coverage_group_coverage.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_coverage_group_coverage.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_coverage_group_coverage.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';





-- ************************************** l_claim_location

CREATE TABLE IF NOT EXISTS l_claim_location
(
 bk_claim         varchar NOT NULL,
 bk_location      varchar NOT NULL,
 cim_load_from_ts timestamp NOT NULL,
 cim_load_to_ts   timestamp NOT NULL,
 cim_invalid_ts   timestamp NULL,
 cim_src_sys_id   integer NOT NULL,
 cim_oe_id        integer NOT NULL,
 CONSTRAINT PK_l_address_claim PRIMARY KEY ( bk_claim, bk_location )
);



COMMENT ON COLUMN l_claim_location.bk_location IS 'Hashvalue generated from business keys of linked tables~OE_ID~Source_SYSTEM_ID';
COMMENT ON COLUMN l_claim_location.cim_load_from_ts IS 'Start-Timestamp of the load. Relevant as part of the key for effectivity satellites and links.';
COMMENT ON COLUMN l_claim_location.cim_load_to_ts IS 'End-Timestamp of the load.';
COMMENT ON COLUMN l_claim_location.cim_invalid_ts IS 'Timestamp at which a row was from technical point of view marked as invalid.';
COMMENT ON COLUMN l_claim_location.cim_src_sys_id IS 'Identifier of the system that the data was provided from.';
COMMENT ON COLUMN l_claim_location.cim_oe_id IS 'Identifier for the Operating Entity (OE) that a row was sourced from.';




