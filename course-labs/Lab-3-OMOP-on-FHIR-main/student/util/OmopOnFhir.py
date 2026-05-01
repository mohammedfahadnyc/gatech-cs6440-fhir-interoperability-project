from sqlalchemy import BigInteger, Column, Date, DateTime, Integer, Numeric, SmallInteger, String, Table, Text, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

t_f_person = Table(
    'f_person', metadata,
    Column('person_id', Integer, nullable=False),
    Column('family_name', String(255)),
    Column('given1_name', String(255)),
    Column('given2_name', String(255)),
    Column('prefix_name', String(255)),
    Column('suffix_name', String(255)),
    Column('preferred_language', String(255)),
    Column('ssn', String(12)),
    Column('active', SmallInteger),
    Column('contact_point1', String(255)),
    Column('contact_point2', String(255)),
    Column('contact_point3', String(255)),
    Column('maritalstatus', String(255))
)

t_care_site = Table(
    'care_site', metadata,
    Column('care_site_id', Integer, nullable=False),
    Column('care_site_name', String(255)),
    Column('place_of_service_concept_id', Integer),
    Column('location_id', Integer),
    Column('care_site_source_value', String(50)),
    Column('place_of_service_source_value', String(50))
)


t_cdm_source = Table(
    'cdm_source', metadata,
    Column('cdm_source_name', String(255), nullable=False),
    Column('cdm_source_abbreviation', String(25), nullable=False),
    Column('cdm_holder', String(255), nullable=False),
    Column('source_description', Text),
    Column('source_documentation_reference', String(255)),
    Column('cdm_etl_reference', String(255)),
    Column('source_release_date', Date, nullable=False),
    Column('cdm_release_date', Date, nullable=False),
    Column('cdm_version', String(10)),
    Column('cdm_version_concept_id', Integer, nullable=False),
    Column('vocabulary_version', String(20), nullable=False)
)

t_cohort = Table(
    'cohort', metadata,
    Column('cohort_definition_id', Integer, nullable=False),
    Column('subject_id', Integer, nullable=False),
    Column('cohort_start_date', Date, nullable=False),
    Column('cohort_end_date', Date, nullable=False)
)


t_cohort_definition = Table(
    'cohort_definition', metadata,
    Column('cohort_definition_id', Integer, nullable=False),
    Column('cohort_definition_name', String(255), nullable=False),
    Column('cohort_definition_description', Text),
    Column('definition_type_concept_id', Integer, nullable=False),
    Column('cohort_definition_syntax', Text),
    Column('subject_concept_id', Integer, nullable=False),
    Column('cohort_initiation_date', Date)
)


t_concept = Table(
    'concept', metadata,
    Column('concept_id', Integer, nullable=False),
    Column('concept_name', String(255), nullable=False),
    Column('domain_id', String(20), nullable=False),
    Column('vocabulary_id', String(20), nullable=False),
    Column('concept_class_id', String(20), nullable=False),
    Column('standard_concept', String(1)),
    Column('concept_code', String(50), nullable=False),
    Column('valid_start_date', Date, nullable=False),
    Column('valid_end_date', Date, nullable=False),
    Column('invalid_reason', String(1))
)


t_concept_ancestor = Table(
    'concept_ancestor', metadata,
    Column('ancestor_concept_id', Integer, nullable=False),
    Column('descendant_concept_id', Integer, nullable=False),
    Column('min_levels_of_separation', Integer, nullable=False),
    Column('max_levels_of_separation', Integer, nullable=False)
)


t_concept_class = Table(
    'concept_class', metadata,
    Column('concept_class_id', String(20), nullable=False),
    Column('concept_class_name', String(255), nullable=False),
    Column('concept_class_concept_id', Integer, nullable=False)
)


t_concept_relationship = Table(
    'concept_relationship', metadata,
    Column('concept_id_1', Integer, nullable=False),
    Column('concept_id_2', Integer, nullable=False),
    Column('relationship_id', String(20), nullable=False),
    Column('valid_start_date', Date, nullable=False),
    Column('valid_end_date', Date, nullable=False),
    Column('invalid_reason', String(1))
)


t_concept_synonym = Table(
    'concept_synonym', metadata,
    Column('concept_id', Integer, nullable=False),
    Column('concept_synonym_name', String(1000), nullable=False),
    Column('language_concept_id', Integer, nullable=False)
)


t_condition_era = Table(
    'condition_era', metadata,
    Column('condition_era_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('condition_concept_id', Integer, nullable=False),
    Column('condition_era_start_date', DateTime, nullable=False),
    Column('condition_era_end_date', DateTime, nullable=False),
    Column('condition_occurrence_count', Integer)
)


t_condition_occurrence = Table(
    'condition_occurrence', metadata,
    Column('condition_occurrence_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('condition_concept_id', Integer, nullable=False),
    Column('condition_start_date', Date, nullable=False),
    Column('condition_start_datetime', DateTime),
    Column('condition_end_date', Date),
    Column('condition_end_datetime', DateTime),
    Column('condition_type_concept_id', Integer, nullable=False),
    Column('condition_status_concept_id', Integer),
    Column('stop_reason', String(20)),
    Column('provider_id', Integer),
    Column('visit_occurrence_id', Integer),
    Column('visit_detail_id', Integer),
    Column('condition_source_value', String(50)),
    Column('condition_source_concept_id', Integer),
    Column('condition_status_source_value', String(50))
)


t_cost = Table(
    'cost', metadata,
    Column('cost_id', Integer, nullable=False),
    Column('cost_event_id', Integer, nullable=False),
    Column('cost_domain_id', String(20), nullable=False),
    Column('cost_type_concept_id', Integer, nullable=False),
    Column('currency_concept_id', Integer),
    Column('total_charge', Numeric),
    Column('total_cost', Numeric),
    Column('total_paid', Numeric),
    Column('paid_by_payer', Numeric),
    Column('paid_by_patient', Numeric),
    Column('paid_patient_copay', Numeric),
    Column('paid_patient_coinsurance', Numeric),
    Column('paid_patient_deductible', Numeric),
    Column('paid_by_primary', Numeric),
    Column('paid_ingredient_cost', Numeric),
    Column('paid_dispensing_fee', Numeric),
    Column('payer_plan_period_id', Integer),
    Column('amount_allowed', Numeric),
    Column('revenue_code_concept_id', Integer),
    Column('revenue_code_source_value', String(50)),
    Column('drg_concept_id', Integer),
    Column('drg_source_value', String(3))
)


t_death = Table(
    'death', metadata,
    Column('person_id', Integer, nullable=False),
    Column('death_date', Date, nullable=False),
    Column('death_datetime', DateTime),
    Column('death_type_concept_id', Integer),
    Column('cause_concept_id', Integer),
    Column('cause_source_value', String(50)),
    Column('cause_source_concept_id', Integer)
)


t_device_exposure = Table(
    'device_exposure', metadata,
    Column('device_exposure_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('device_concept_id', Integer, nullable=False),
    Column('device_exposure_start_date', Date, nullable=False),
    Column('device_exposure_start_datetime', DateTime),
    Column('device_exposure_end_date', Date),
    Column('device_exposure_end_datetime', DateTime),
    Column('device_type_concept_id', Integer, nullable=False),
    Column('unique_device_id', String(255)),
    Column('production_id', String(255)),
    Column('quantity', Integer),
    Column('provider_id', Integer),
    Column('visit_occurrence_id', Integer),
    Column('visit_detail_id', Integer),
    Column('device_source_value', String(50)),
    Column('device_source_concept_id', Integer),
    Column('unit_concept_id', Integer),
    Column('unit_source_value', String(50)),
    Column('unit_source_concept_id', Integer)
)


t_domain = Table(
    'domain', metadata,
    Column('domain_id', String(20), nullable=False),
    Column('domain_name', String(255), nullable=False),
    Column('domain_concept_id', Integer, nullable=False)
)


t_dose_era = Table(
    'dose_era', metadata,
    Column('dose_era_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('drug_concept_id', Integer, nullable=False),
    Column('unit_concept_id', Integer, nullable=False),
    Column('dose_value', Numeric, nullable=False),
    Column('dose_era_start_date', DateTime, nullable=False),
    Column('dose_era_end_date', DateTime, nullable=False)
)


t_drug_era = Table(
    'drug_era', metadata,
    Column('drug_era_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('drug_concept_id', Integer, nullable=False),
    Column('drug_era_start_date', DateTime, nullable=False),
    Column('drug_era_end_date', DateTime, nullable=False),
    Column('drug_exposure_count', Integer),
    Column('gap_days', Integer)
)


t_drug_exposure = Table(
    'drug_exposure', metadata,
    Column('drug_exposure_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('drug_concept_id', Integer, nullable=False),
    Column('drug_exposure_start_date', Date, nullable=False),
    Column('drug_exposure_start_datetime', DateTime),
    Column('drug_exposure_end_date', Date, nullable=False),
    Column('drug_exposure_end_datetime', DateTime),
    Column('verbatim_end_date', Date),
    Column('drug_type_concept_id', Integer, nullable=False),
    Column('stop_reason', String(20)),
    Column('refills', Integer),
    Column('quantity', Numeric),
    Column('days_supply', Integer),
    Column('sig', Text),
    Column('route_concept_id', Integer),
    Column('lot_number', String(50)),
    Column('provider_id', Integer),
    Column('visit_occurrence_id', Integer),
    Column('visit_detail_id', Integer),
    Column('drug_source_value', String(50)),
    Column('drug_source_concept_id', Integer),
    Column('route_source_value', String(50)),
    Column('dose_unit_source_value', String(50))
)


t_drug_strength = Table(
    'drug_strength', metadata,
    Column('drug_concept_id', Integer, nullable=False),
    Column('ingredient_concept_id', Integer, nullable=False),
    Column('amount_value', Numeric),
    Column('amount_unit_concept_id', Integer),
    Column('numerator_value', Numeric),
    Column('numerator_unit_concept_id', Integer),
    Column('denominator_value', Numeric),
    Column('denominator_unit_concept_id', Integer),
    Column('box_size', Integer),
    Column('valid_start_date', Date, nullable=False),
    Column('valid_end_date', Date, nullable=False),
    Column('invalid_reason', String(1))
)


t_episode = Table(
    'episode', metadata,
    Column('episode_id', BigInteger, nullable=False),
    Column('person_id', BigInteger, nullable=False),
    Column('episode_concept_id', Integer, nullable=False),
    Column('episode_start_date', Date, nullable=False),
    Column('episode_start_datetime', DateTime),
    Column('episode_end_date', Date),
    Column('episode_end_datetime', DateTime),
    Column('episode_parent_id', BigInteger),
    Column('episode_number', Integer),
    Column('episode_object_concept_id', Integer, nullable=False),
    Column('episode_type_concept_id', Integer, nullable=False),
    Column('episode_source_value', String(50)),
    Column('episode_source_concept_id', Integer)
)


t_episode_event = Table(
    'episode_event', metadata,
    Column('episode_id', BigInteger, nullable=False),
    Column('event_id', BigInteger, nullable=False),
    Column('episode_event_field_concept_id', Integer, nullable=False)
)


class FCache(Base):
    __tablename__ = 'f_cache'

    cache_id = Column(Integer, primary_key=True)
    key_text = Column(Text, nullable=False)
    value_text = Column(Text)
    value_int = Column(Integer)
    status = Column(Integer, server_default=text("'-1'::integer"))


t_f_immunization_view = Table(
    'f_immunization_view', metadata,
    Column('immunization_id', Integer),
    Column('person_id', Integer),
    Column('immunization_concept_id', Integer),
    Column('immunization_date', Date),
    Column('immunization_datetime', DateTime),
    Column('immunization_type_concept_id', Integer),
    Column('immunization_status', String),
    Column('provider_id', Integer),
    Column('visit_occurrence_id', Integer),
    Column('lot_number', String),
    Column('route_concept_id', Integer),
    Column('quantity', Numeric),
    Column('immunization_note', Text)
)


t_f_observation_view = Table(
    'f_observation_view', metadata,
    Column('observation_id', Integer),
    Column('person_id', Integer),
    Column('observation_concept_id', Integer),
    Column('observation_date', Date),
    Column('observation_datetime', DateTime),
    Column('observation_time', String),
    Column('observation_type_concept_id', Integer),
    Column('observation_operator_concept_id', Integer),
    Column('value_as_number', Numeric),
    Column('value_as_string', String),
    Column('value_as_concept_id', Integer),
    Column('qualifier_concept_id', Integer),
    Column('unit_concept_id', Integer),
    Column('range_low', Numeric),
    Column('range_high', Numeric),
    Column('provider_id', Integer),
    Column('visit_occurrence_id', Integer),
    Column('visit_detail_id', Integer),
    Column('observation_source_value', String(50)),
    Column('observation_source_concept_id', Integer),
    Column('unit_source_value', String(50)),
    Column('qualifier_source_value', String),
    Column('unit_source_concept_id', Integer),
    Column('value_source_value', String(50)),
    Column('observation_event_id', BigInteger),
    Column('obs_event_field_concept_id', Integer)
)



t_fact_relationship = Table(
    'fact_relationship', metadata,
    Column('domain_concept_id_1', Integer, nullable=False),
    Column('fact_id_1', Integer, nullable=False),
    Column('domain_concept_id_2', Integer, nullable=False),
    Column('fact_id_2', Integer, nullable=False),
    Column('relationship_concept_id', Integer, nullable=False)
)


t_location = Table(
    'location', metadata,
    Column('location_id', Integer, nullable=False),
    Column('address_1', String(50)),
    Column('address_2', String(50)),
    Column('city', String(50)),
    Column('state', String(2)),
    Column('zip', String(9)),
    Column('county', String(20)),
    Column('location_source_value', String(50)),
    Column('country_concept_id', Integer),
    Column('country_source_value', String(80)),
    Column('latitude', Numeric),
    Column('longitude', Numeric)
)


t_measurement = Table(
    'measurement', metadata,
    Column('measurement_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('measurement_concept_id', Integer, nullable=False),
    Column('measurement_date', Date, nullable=False),
    Column('measurement_datetime', DateTime),
    Column('measurement_time', String(10)),
    Column('measurement_type_concept_id', Integer, nullable=False),
    Column('operator_concept_id', Integer),
    Column('value_as_number', Numeric),
    Column('value_as_concept_id', Integer),
    Column('unit_concept_id', Integer),
    Column('range_low', Numeric),
    Column('range_high', Numeric),
    Column('provider_id', Integer),
    Column('visit_occurrence_id', Integer),
    Column('visit_detail_id', Integer),
    Column('measurement_source_value', String(50)),
    Column('measurement_source_concept_id', Integer),
    Column('unit_source_value', String(50)),
    Column('unit_source_concept_id', Integer),
    Column('value_source_value', String(50)),
    Column('measurement_event_id', BigInteger),
    Column('meas_event_field_concept_id', Integer)
)


t_metadata_ = Table(
    'metadata', metadata,
    Column('metadata_id', Integer, nullable=False),
    Column('metadata_concept_id', Integer, nullable=False),
    Column('metadata_type_concept_id', Integer, nullable=False),
    Column('name', String(250), nullable=False),
    Column('value_as_string', String(250)),
    Column('value_as_concept_id', Integer),
    Column('value_as_number', Numeric),
    Column('metadata_date', Date),
    Column('metadata_datetime', DateTime)
)


t_note = Table(
    'note', metadata,
    Column('note_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('note_date', Date, nullable=False),
    Column('note_datetime', DateTime),
    Column('note_type_concept_id', Integer, nullable=False),
    Column('note_class_concept_id', Integer, nullable=False),
    Column('note_title', String(250)),
    Column('note_text', Text, nullable=False),
    Column('encoding_concept_id', Integer, nullable=False),
    Column('language_concept_id', Integer, nullable=False),
    Column('provider_id', Integer),
    Column('visit_occurrence_id', Integer),
    Column('visit_detail_id', Integer),
    Column('note_source_value', String(50)),
    Column('note_event_id', BigInteger),
    Column('note_event_field_concept_id', Integer)
)


t_note_nlp = Table(
    'note_nlp', metadata,
    Column('note_nlp_id', Integer, nullable=False),
    Column('note_id', Integer, nullable=False),
    Column('section_concept_id', Integer),
    Column('snippet', String(250)),
    Column('offset', String(50)),
    Column('lexical_variant', String(250), nullable=False),
    Column('note_nlp_concept_id', Integer),
    Column('note_nlp_source_concept_id', Integer),
    Column('nlp_system', String(250)),
    Column('nlp_date', Date, nullable=False),
    Column('nlp_datetime', DateTime),
    Column('term_exists', String(1)),
    Column('term_temporal', String(50)),
    Column('term_modifiers', String(2000))
)


t_observation = Table(
    'observation', metadata,
    Column('observation_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('observation_concept_id', Integer, nullable=False),
    Column('observation_date', Date, nullable=False),
    Column('observation_datetime', DateTime),
    Column('observation_type_concept_id', Integer, nullable=False),
    Column('value_as_number', Numeric),
    Column('value_as_string', String(60)),
    Column('value_as_concept_id', Integer),
    Column('qualifier_concept_id', Integer),
    Column('unit_concept_id', Integer),
    Column('provider_id', Integer),
    Column('visit_occurrence_id', Integer),
    Column('visit_detail_id', Integer),
    Column('observation_source_value', String(50)),
    Column('observation_source_concept_id', Integer),
    Column('unit_source_value', String(50)),
    Column('qualifier_source_value', String(50)),
    Column('value_source_value', String(50)),
    Column('observation_event_id', BigInteger),
    Column('obs_event_field_concept_id', Integer)
)


t_observation_period = Table(
    'observation_period', metadata,
    Column('observation_period_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('observation_period_start_date', Date, nullable=False),
    Column('observation_period_end_date', Date, nullable=False),
    Column('period_type_concept_id', Integer, nullable=False)
)


t_payer_plan_period = Table(
    'payer_plan_period', metadata,
    Column('payer_plan_period_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('payer_plan_period_start_date', Date, nullable=False),
    Column('payer_plan_period_end_date', Date, nullable=False),
    Column('payer_concept_id', Integer),
    Column('payer_source_value', String(50)),
    Column('payer_source_concept_id', Integer),
    Column('plan_concept_id', Integer),
    Column('plan_source_value', String(50)),
    Column('plan_source_concept_id', Integer),
    Column('sponsor_concept_id', Integer),
    Column('sponsor_source_value', String(50)),
    Column('sponsor_source_concept_id', Integer),
    Column('family_source_value', String(50)),
    Column('stop_reason_concept_id', Integer),
    Column('stop_reason_source_value', String(50)),
    Column('stop_reason_source_concept_id', Integer)
)


t_person = Table(
    'person', metadata,
    Column('person_id', Integer, nullable=False),
    Column('gender_concept_id', Integer, nullable=False),
    Column('year_of_birth', Integer, nullable=False),
    Column('month_of_birth', Integer),
    Column('day_of_birth', Integer),
    Column('birth_datetime', DateTime),
    Column('race_concept_id', Integer, nullable=False),
    Column('ethnicity_concept_id', Integer, nullable=False),
    Column('location_id', Integer),
    Column('provider_id', Integer),
    Column('care_site_id', Integer),
    Column('person_source_value', String(50)),
    Column('gender_source_value', String(50)),
    Column('gender_source_concept_id', Integer),
    Column('race_source_value', String(50)),
    Column('race_source_concept_id', Integer),
    Column('ethnicity_source_value', String(50)),
    Column('ethnicity_source_concept_id', Integer)
)


t_procedure_occurrence = Table(
    'procedure_occurrence', metadata,
    Column('procedure_occurrence_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('procedure_concept_id', Integer, nullable=False),
    Column('procedure_date', Date, nullable=False),
    Column('procedure_datetime', DateTime),
    Column('procedure_end_date', Date),
    Column('procedure_end_datetime', DateTime),
    Column('procedure_type_concept_id', Integer, nullable=False),
    Column('modifier_concept_id', Integer),
    Column('quantity', Integer),
    Column('provider_id', Integer),
    Column('visit_occurrence_id', Integer),
    Column('visit_detail_id', Integer),
    Column('procedure_source_value', String(50)),
    Column('procedure_source_concept_id', Integer),
    Column('modifier_source_value', String(50))
)


t_provider = Table(
    'provider', metadata,
    Column('provider_id', Integer, nullable=False),
    Column('provider_name', String(255)),
    Column('npi', String(20)),
    Column('dea', String(20)),
    Column('specialty_concept_id', Integer),
    Column('care_site_id', Integer),
    Column('year_of_birth', Integer),
    Column('gender_concept_id', Integer),
    Column('provider_source_value', String(50)),
    Column('specialty_source_value', String(50)),
    Column('specialty_source_concept_id', Integer),
    Column('gender_source_value', String(50)),
    Column('gender_source_concept_id', Integer)
)


t_relationship = Table(
    'relationship', metadata,
    Column('relationship_id', String(20), nullable=False),
    Column('relationship_name', String(255), nullable=False),
    Column('is_hierarchical', String(1), nullable=False),
    Column('defines_ancestry', String(1), nullable=False),
    Column('reverse_relationship_id', String(20), nullable=False),
    Column('relationship_concept_id', Integer, nullable=False)
)


t_source_to_concept_map = Table(
    'source_to_concept_map', metadata,
    Column('source_code', String(50), nullable=False),
    Column('source_concept_id', Integer, nullable=False),
    Column('source_vocabulary_id', String(20), nullable=False),
    Column('source_code_description', String(255)),
    Column('target_concept_id', Integer, nullable=False),
    Column('target_vocabulary_id', String(20), nullable=False),
    Column('valid_start_date', Date, nullable=False),
    Column('valid_end_date', Date, nullable=False),
    Column('invalid_reason', String(1))
)


t_specimen = Table(
    'specimen', metadata,
    Column('specimen_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('specimen_concept_id', Integer, nullable=False),
    Column('specimen_type_concept_id', Integer, nullable=False),
    Column('specimen_date', Date, nullable=False),
    Column('specimen_datetime', DateTime),
    Column('quantity', Numeric),
    Column('unit_concept_id', Integer),
    Column('anatomic_site_concept_id', Integer),
    Column('disease_status_concept_id', Integer),
    Column('specimen_source_id', String(50)),
    Column('specimen_source_value', String(50)),
    Column('unit_source_value', String(50)),
    Column('anatomic_site_source_value', String(50)),
    Column('disease_status_source_value', String(50))
)


t_visit_detail = Table(
    'visit_detail', metadata,
    Column('visit_detail_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('visit_detail_concept_id', Integer, nullable=False),
    Column('visit_detail_start_date', Date, nullable=False),
    Column('visit_detail_start_datetime', DateTime),
    Column('visit_detail_end_date', Date, nullable=False),
    Column('visit_detail_end_datetime', DateTime),
    Column('visit_detail_type_concept_id', Integer, nullable=False),
    Column('provider_id', Integer),
    Column('care_site_id', Integer),
    Column('visit_detail_source_value', String(50)),
    Column('visit_detail_source_concept_id', Integer),
    Column('admitted_from_concept_id', Integer),
    Column('admitted_from_source_value', String(50)),
    Column('discharged_to_source_value', String(50)),
    Column('discharged_to_concept_id', Integer),
    Column('preceding_visit_detail_id', Integer),
    Column('parent_visit_detail_id', Integer),
    Column('visit_occurrence_id', Integer, nullable=False)
)


t_visit_occurrence = Table(
    'visit_occurrence', metadata,
    Column('visit_occurrence_id', Integer, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('visit_concept_id', Integer, nullable=False),
    Column('visit_start_date', Date, nullable=False),
    Column('visit_start_datetime', DateTime),
    Column('visit_end_date', Date, nullable=False),
    Column('visit_end_datetime', DateTime),
    Column('visit_type_concept_id', Integer, nullable=False),
    Column('provider_id', Integer),
    Column('care_site_id', Integer),
    Column('visit_source_value', String(50)),
    Column('visit_source_concept_id', Integer),
    Column('admitted_from_concept_id', Integer),
    Column('admitted_from_source_value', String(50)),
    Column('discharged_to_concept_id', Integer),
    Column('discharged_to_source_value', String(50)),
    Column('preceding_visit_occurrence_id', Integer)
)


t_vocabulary = Table(
    'vocabulary', metadata,
    Column('vocabulary_id', String(20), nullable=False),
    Column('vocabulary_name', String(255), nullable=False),
    Column('vocabulary_reference', String(255)),
    Column('vocabulary_version', String(255)),
    Column('vocabulary_concept_id', Integer, nullable=False)
)
