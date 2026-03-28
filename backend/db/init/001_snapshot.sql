--
-- PostgreSQL database dump
--

\restrict bh74ikf2mYE8StGZ12oUVlMLbiaTd79J1beV1seJfgg6ufRa0H8BOGt5YNdHI11

-- Dumped from database version 16.13
-- Dumped by pg_dump version 16.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_patient_id_fkey;
ALTER TABLE IF EXISTS ONLY public.fhir_resources DROP CONSTRAINT IF EXISTS fhir_resources_patient_id_fkey;
DROP INDEX IF EXISTS public.ix_users_role;
DROP INDEX IF EXISTS public.ix_users_email;
DROP INDEX IF EXISTS public.ix_fhir_resources_resource_type;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.patients DROP CONSTRAINT IF EXISTS patients_pkey;
ALTER TABLE IF EXISTS ONLY public.fhir_resources DROP CONSTRAINT IF EXISTS fhir_resources_pkey;
ALTER TABLE IF EXISTS public.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.patients ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.fhir_resources ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.users_id_seq;
DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.patients_id_seq;
DROP TABLE IF EXISTS public.patients;
DROP SEQUENCE IF EXISTS public.fhir_resources_id_seq;
DROP TABLE IF EXISTS public.fhir_resources;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: fhir_resources; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fhir_resources (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    resource_type character varying(80) NOT NULL,
    payload_json jsonb NOT NULL,
    source_system character varying(100) NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: fhir_resources_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.fhir_resources_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fhir_resources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.fhir_resources_id_seq OWNED BY public.fhir_resources.id;


--
-- Name: patients; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.patients (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    dob date NOT NULL,
    gender character varying(50) NOT NULL,
    is_authorized boolean NOT NULL,
    is_imported boolean NOT NULL,
    data_source character varying(100),
    data_origin character varying(50) NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: patients_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.patients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: patients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.patients_id_seq OWNED BY public.patients.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(50) NOT NULL,
    patient_id integer,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: fhir_resources id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fhir_resources ALTER COLUMN id SET DEFAULT nextval('public.fhir_resources_id_seq'::regclass);


--
-- Name: patients id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patients ALTER COLUMN id SET DEFAULT nextval('public.patients_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: fhir_resources; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.fhir_resources VALUES (1, 1, 'Patient', '{"id": "patient-1", "name": [{"text": "George Burdell"}], "gender": "male", "birthDate": "1978-04-12", "resourceType": "Patient"}', 'internal', '2026-03-28 23:25:19.057587+00');
INSERT INTO public.fhir_resources VALUES (2, 1, 'Condition', '{"id": "21918700-5332-4ae3-81d9-8c7be5aad704", "code": {"text": "Type 2 Diabetes Mellitus"}, "subject": {"reference": "Patient/1"}, "recordedDate": "2025-04-04", "resourceType": "Condition", "clinicalStatus": {"text": "active"}}', 'internal', '2026-03-28 23:25:19.057593+00');
INSERT INTO public.fhir_resources VALUES (3, 1, 'Observation', '{"id": "c4a16f99-32da-4626-bca4-7e4087a8d910", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/1"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 5.7}, "effectiveDateTime": "2025-03-31"}', 'internal', '2026-03-28 23:25:19.057594+00');
INSERT INTO public.fhir_resources VALUES (4, 1, 'Observation', '{"id": "aeea4a73-62eb-416b-9347-262a68b9ad13", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/1"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 6.2}, "effectiveDateTime": "2025-06-29"}', 'internal', '2026-03-28 23:25:19.057594+00');
INSERT INTO public.fhir_resources VALUES (5, 1, 'Observation', '{"id": "31a1eec1-82cf-4c05-bf8d-74c99722a5c5", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/1"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 7.1}, "effectiveDateTime": "2025-09-27"}', 'internal', '2026-03-28 23:25:19.057595+00');
INSERT INTO public.fhir_resources VALUES (6, 1, 'Observation', '{"id": "eddaf2ca-2e71-4b74-910a-12dbf9a7a0d0", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/1"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 7.8}, "effectiveDateTime": "2025-12-26"}', 'internal', '2026-03-28 23:25:19.057595+00');
INSERT INTO public.fhir_resources VALUES (7, 1, 'Observation', '{"id": "87b51079-c192-4fc7-b32d-c78b9fa7be76", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/1"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 8.4}, "effectiveDateTime": "2026-03-26"}', 'internal', '2026-03-28 23:25:19.057595+00');
INSERT INTO public.fhir_resources VALUES (8, 1, 'MedicationStatement', '{"id": "5bb3ac0b-3b3c-454b-98f4-4547bfd07048", "status": "active", "subject": {"reference": "Patient/1"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-04-02", "medicationCodeableConcept": {"text": "Metformin"}}', 'internal', '2026-03-28 23:25:19.057596+00');
INSERT INTO public.fhir_resources VALUES (9, 1, 'MedicationStatement', '{"id": "4784a2e4-ef86-4147-b8d0-f0b7f4d92c54", "status": "active", "subject": {"reference": "Patient/1"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-06-01", "medicationCodeableConcept": {"text": "Jardiance"}}', 'internal', '2026-03-28 23:25:19.057596+00');
INSERT INTO public.fhir_resources VALUES (10, 1, 'MedicationStatement', '{"id": "4f70d48f-3bdf-4972-a95a-a7281a79aa75", "status": "active", "subject": {"reference": "Patient/1"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-07-31", "medicationCodeableConcept": {"text": "Trulicity"}}', 'internal', '2026-03-28 23:25:19.057597+00');
INSERT INTO public.fhir_resources VALUES (11, 1, 'MedicationStatement', '{"id": "011f9a2e-fc84-4aaa-a6d8-a41a97678095", "status": "active", "subject": {"reference": "Patient/1"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-09-29", "medicationCodeableConcept": {"text": "Prednisone"}}', 'internal', '2026-03-28 23:25:19.057597+00');
INSERT INTO public.fhir_resources VALUES (12, 1, 'DocumentReference', '{"id": "1b79b125-8683-46b0-b289-8c37ac305bc2", "date": "2026-03-28T23:25:19.055421+00:00", "author": [{"display": "doctor1@clinic.com"}], "status": "current", "content": [{"attachment": {"data": "R2VvcmdlIEJ1cmRlbGwgZGlhYmV0ZXMgZm9sbG93LXVwIG5vdGUuIEVuY291cmFnZSBkaWV0IGFkaGVyZW5jZSBhbmQgZXhlcmNpc2Uu", "contentType": "text/plain"}}], "subject": {"reference": "Patient/1"}, "description": "Clinical note", "resourceType": "DocumentReference"}', 'internal', '2026-03-28 23:25:19.057598+00');
INSERT INTO public.fhir_resources VALUES (13, 2, 'Patient', '{"id": "patient-2", "name": [{"text": "Maria Lopez"}], "gender": "female", "birthDate": "1985-07-23", "resourceType": "Patient"}', 'internal', '2026-03-28 23:25:19.179571+00');
INSERT INTO public.fhir_resources VALUES (14, 2, 'Condition', '{"id": "de495e94-bbe1-45d5-964d-9d9ae7e6a6fb", "code": {"text": "Type 2 Diabetes Mellitus"}, "subject": {"reference": "Patient/2"}, "recordedDate": "2025-04-11", "resourceType": "Condition", "clinicalStatus": {"text": "active"}}', 'internal', '2026-03-28 23:25:19.179572+00');
INSERT INTO public.fhir_resources VALUES (15, 2, 'Observation', '{"id": "92d5969d-a246-4110-923a-2a93e2d730b4", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/2"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 5.7}, "effectiveDateTime": "2025-04-03"}', 'internal', '2026-03-28 23:25:19.179573+00');
INSERT INTO public.fhir_resources VALUES (16, 2, 'Observation', '{"id": "e9422d55-82b1-4295-a5b4-eefc2f6cb657", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/2"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 6.2}, "effectiveDateTime": "2025-07-02"}', 'internal', '2026-03-28 23:25:19.179573+00');
INSERT INTO public.fhir_resources VALUES (17, 2, 'Observation', '{"id": "f983b220-c115-4e8b-8628-c70bb6f31e8f", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/2"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 7.1}, "effectiveDateTime": "2025-09-30"}', 'internal', '2026-03-28 23:25:19.179574+00');
INSERT INTO public.fhir_resources VALUES (18, 2, 'Observation', '{"id": "14793ba1-bd5d-491b-a7af-621238b49bc1", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/2"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 7.8}, "effectiveDateTime": "2025-12-29"}', 'internal', '2026-03-28 23:25:19.179574+00');
INSERT INTO public.fhir_resources VALUES (19, 2, 'Observation', '{"id": "8951da0f-ffbc-43ef-8485-6e1545f63308", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/2"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 8.4}, "effectiveDateTime": "2026-03-29"}', 'internal', '2026-03-28 23:25:19.179574+00');
INSERT INTO public.fhir_resources VALUES (20, 2, 'MedicationStatement', '{"id": "6ed1762b-73b2-4996-83da-13f39e21c2e1", "status": "active", "subject": {"reference": "Patient/2"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-04-07", "medicationCodeableConcept": {"text": "Metformin"}}', 'internal', '2026-03-28 23:25:19.179575+00');
INSERT INTO public.fhir_resources VALUES (21, 2, 'MedicationStatement', '{"id": "b8e5280e-c31c-49b5-bf4d-07864328552e", "status": "active", "subject": {"reference": "Patient/2"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-06-06", "medicationCodeableConcept": {"text": "Jardiance"}}', 'internal', '2026-03-28 23:25:19.179575+00');
INSERT INTO public.fhir_resources VALUES (22, 2, 'MedicationStatement', '{"id": "c56a5410-e063-4899-8374-a8eea101c740", "status": "active", "subject": {"reference": "Patient/2"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-08-05", "medicationCodeableConcept": {"text": "Trulicity"}}', 'internal', '2026-03-28 23:25:19.179576+00');
INSERT INTO public.fhir_resources VALUES (23, 2, 'MedicationStatement', '{"id": "cd6731b1-04d3-4acd-83e0-67b5a9b0dcc8", "status": "active", "subject": {"reference": "Patient/2"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-10-04", "medicationCodeableConcept": {"text": "Prednisone"}}', 'internal', '2026-03-28 23:25:19.179576+00');
INSERT INTO public.fhir_resources VALUES (24, 2, 'DocumentReference', '{"id": "521723ed-5199-4962-bde4-b629e5a92989", "date": "2026-03-28T23:25:19.177939+00:00", "author": [{"display": "doctor1@clinic.com"}], "status": "current", "content": [{"attachment": {"data": "TWFyaWEgTG9wZXogZGlhYmV0ZXMgZm9sbG93LXVwIG5vdGUuIEVuY291cmFnZSBkaWV0IGFkaGVyZW5jZSBhbmQgZXhlcmNpc2Uu", "contentType": "text/plain"}}], "subject": {"reference": "Patient/2"}, "description": "Clinical note", "resourceType": "DocumentReference"}', 'internal', '2026-03-28 23:25:19.179576+00');
INSERT INTO public.fhir_resources VALUES (25, 3, 'Patient', '{"id": "patient-3", "name": [{"text": "David Chen"}], "gender": "male", "birthDate": "1969-11-02", "resourceType": "Patient"}', 'internal', '2026-03-28 23:25:19.299675+00');
INSERT INTO public.fhir_resources VALUES (26, 3, 'Condition', '{"id": "e2542da5-90da-43db-9d2c-42c25318a824", "code": {"text": "Type 2 Diabetes Mellitus"}, "subject": {"reference": "Patient/3"}, "recordedDate": "2025-04-18", "resourceType": "Condition", "clinicalStatus": {"text": "active"}}', 'internal', '2026-03-28 23:25:19.299676+00');
INSERT INTO public.fhir_resources VALUES (27, 3, 'Observation', '{"id": "74d6c5b9-9f08-46a1-86ab-4032fc67e6ac", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/3"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 5.7}, "effectiveDateTime": "2025-04-06"}', 'internal', '2026-03-28 23:25:19.299676+00');
INSERT INTO public.fhir_resources VALUES (28, 3, 'Observation', '{"id": "b2decea8-8cf0-48d8-936e-9631ab81c676", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/3"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 6.2}, "effectiveDateTime": "2025-07-05"}', 'internal', '2026-03-28 23:25:19.299677+00');
INSERT INTO public.fhir_resources VALUES (29, 3, 'Observation', '{"id": "749c47f0-462b-4cbc-a79b-806215aea332", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/3"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 7.1}, "effectiveDateTime": "2025-10-03"}', 'internal', '2026-03-28 23:25:19.299677+00');
INSERT INTO public.fhir_resources VALUES (30, 3, 'Observation', '{"id": "77bdf133-068f-4d1c-9844-c73d96423b47", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/3"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 7.8}, "effectiveDateTime": "2026-01-01"}', 'internal', '2026-03-28 23:25:19.299677+00');
INSERT INTO public.fhir_resources VALUES (31, 3, 'Observation', '{"id": "c888744a-14a7-426f-a308-4e0acd6fa719", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/3"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 8.4}, "effectiveDateTime": "2026-04-01"}', 'internal', '2026-03-28 23:25:19.299678+00');
INSERT INTO public.fhir_resources VALUES (32, 3, 'MedicationStatement', '{"id": "dc8b4add-9449-4ed3-a6c3-03b37086d23f", "status": "active", "subject": {"reference": "Patient/3"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-04-12", "medicationCodeableConcept": {"text": "Metformin"}}', 'internal', '2026-03-28 23:25:19.299678+00');
INSERT INTO public.fhir_resources VALUES (33, 3, 'MedicationStatement', '{"id": "c00886ac-4d0f-4008-b074-d88c8cf11480", "status": "active", "subject": {"reference": "Patient/3"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-06-11", "medicationCodeableConcept": {"text": "Jardiance"}}', 'internal', '2026-03-28 23:25:19.299679+00');
INSERT INTO public.fhir_resources VALUES (34, 3, 'MedicationStatement', '{"id": "58b1a2fa-0d96-463d-bddd-fdd35a9d7851", "status": "active", "subject": {"reference": "Patient/3"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-08-10", "medicationCodeableConcept": {"text": "Trulicity"}}', 'internal', '2026-03-28 23:25:19.299679+00');
INSERT INTO public.fhir_resources VALUES (35, 3, 'MedicationStatement', '{"id": "d62c7d13-b2aa-45a0-850b-808918f13f5c", "status": "active", "subject": {"reference": "Patient/3"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-10-09", "medicationCodeableConcept": {"text": "Prednisone"}}', 'internal', '2026-03-28 23:25:19.299679+00');
INSERT INTO public.fhir_resources VALUES (36, 3, 'DocumentReference', '{"id": "5a969cf4-5b2e-4fd9-8855-352022d041b6", "date": "2026-03-28T23:25:19.298107+00:00", "author": [{"display": "doctor1@clinic.com"}], "status": "current", "content": [{"attachment": {"data": "RGF2aWQgQ2hlbiBkaWFiZXRlcyBmb2xsb3ctdXAgbm90ZS4gRW5jb3VyYWdlIGRpZXQgYWRoZXJlbmNlIGFuZCBleGVyY2lzZS4=", "contentType": "text/plain"}}], "subject": {"reference": "Patient/3"}, "description": "Clinical note", "resourceType": "DocumentReference"}', 'internal', '2026-03-28 23:25:19.29968+00');
INSERT INTO public.fhir_resources VALUES (37, 4, 'Patient', '{"id": "patient-4", "name": [{"text": "Sarah Kim"}], "gender": "female", "birthDate": "1990-01-14", "resourceType": "Patient"}', 'internal', '2026-03-28 23:25:19.421058+00');
INSERT INTO public.fhir_resources VALUES (38, 4, 'Condition', '{"id": "00184fe0-793d-4131-8ba3-abffc9642380", "code": {"text": "Type 2 Diabetes Mellitus"}, "subject": {"reference": "Patient/4"}, "recordedDate": "2025-04-25", "resourceType": "Condition", "clinicalStatus": {"text": "active"}}', 'internal', '2026-03-28 23:25:19.421059+00');
INSERT INTO public.fhir_resources VALUES (39, 4, 'Observation', '{"id": "2d52decc-9ee8-45e1-bf57-d2efb3f217b3", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/4"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 5.7}, "effectiveDateTime": "2025-04-09"}', 'internal', '2026-03-28 23:25:19.42106+00');
INSERT INTO public.fhir_resources VALUES (40, 4, 'Observation', '{"id": "6e3b8c33-3dbd-4f69-9168-b5233ae9cbdf", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/4"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 6.2}, "effectiveDateTime": "2025-07-08"}', 'internal', '2026-03-28 23:25:19.42106+00');
INSERT INTO public.fhir_resources VALUES (41, 4, 'Observation', '{"id": "e114c2a8-8855-4e84-b859-20f7c5f9b102", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/4"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 7.1}, "effectiveDateTime": "2025-10-06"}', 'internal', '2026-03-28 23:25:19.421061+00');
INSERT INTO public.fhir_resources VALUES (42, 4, 'Observation', '{"id": "a1f2d9e5-ee3c-4d63-ae85-fc1147ab2878", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/4"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 7.8}, "effectiveDateTime": "2026-01-04"}', 'internal', '2026-03-28 23:25:19.421061+00');
INSERT INTO public.fhir_resources VALUES (43, 4, 'Observation', '{"id": "018de1ff-0b9f-40a9-8acf-d3aa1c03ae71", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/4"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 8.4}, "effectiveDateTime": "2026-04-04"}', 'internal', '2026-03-28 23:25:19.421061+00');
INSERT INTO public.fhir_resources VALUES (44, 4, 'MedicationStatement', '{"id": "536a2276-46e9-40a1-881c-44e9781e664f", "status": "active", "subject": {"reference": "Patient/4"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-04-17", "medicationCodeableConcept": {"text": "Metformin"}}', 'internal', '2026-03-28 23:25:19.421062+00');
INSERT INTO public.fhir_resources VALUES (45, 4, 'MedicationStatement', '{"id": "4327b5e9-acb3-4e0e-a2a2-9b5660a129ae", "status": "active", "subject": {"reference": "Patient/4"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-06-16", "medicationCodeableConcept": {"text": "Jardiance"}}', 'internal', '2026-03-28 23:25:19.421062+00');
INSERT INTO public.fhir_resources VALUES (46, 4, 'MedicationStatement', '{"id": "dddd6281-6588-401d-b9d1-572742e5e2aa", "status": "active", "subject": {"reference": "Patient/4"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-08-15", "medicationCodeableConcept": {"text": "Trulicity"}}', 'internal', '2026-03-28 23:25:19.421062+00');
INSERT INTO public.fhir_resources VALUES (47, 4, 'MedicationStatement', '{"id": "b38aec73-6d4a-4cab-bbe7-5cf679e379b7", "status": "active", "subject": {"reference": "Patient/4"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-10-14", "medicationCodeableConcept": {"text": "Prednisone"}}', 'internal', '2026-03-28 23:25:19.421063+00');
INSERT INTO public.fhir_resources VALUES (48, 4, 'DocumentReference', '{"id": "10e3537d-2af9-4e5c-925c-869753ea6244", "date": "2026-03-28T23:25:19.419096+00:00", "author": [{"display": "doctor1@clinic.com"}], "status": "current", "content": [{"attachment": {"data": "U2FyYWggS2ltIGRpYWJldGVzIGZvbGxvdy11cCBub3RlLiBFbmNvdXJhZ2UgZGlldCBhZGhlcmVuY2UgYW5kIGV4ZXJjaXNlLg==", "contentType": "text/plain"}}], "subject": {"reference": "Patient/4"}, "description": "Clinical note", "resourceType": "DocumentReference"}', 'internal', '2026-03-28 23:25:19.421063+00');
INSERT INTO public.fhir_resources VALUES (49, 5, 'Patient', '{"id": "patient-5", "name": [{"text": "John Patel"}], "gender": "male", "birthDate": "1975-09-30", "resourceType": "Patient"}', 'internal', '2026-03-28 23:25:19.540682+00');
INSERT INTO public.fhir_resources VALUES (50, 5, 'Condition', '{"id": "fc94d812-3ccf-4e82-bd98-3b3175944ae3", "code": {"text": "Type 2 Diabetes Mellitus"}, "subject": {"reference": "Patient/5"}, "recordedDate": "2025-05-02", "resourceType": "Condition", "clinicalStatus": {"text": "active"}}', 'internal', '2026-03-28 23:25:19.540684+00');
INSERT INTO public.fhir_resources VALUES (51, 5, 'Observation', '{"id": "b7cf6f71-f786-4900-bc50-460b49ba922e", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/5"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 5.7}, "effectiveDateTime": "2025-04-12"}', 'internal', '2026-03-28 23:25:19.540684+00');
INSERT INTO public.fhir_resources VALUES (52, 5, 'Observation', '{"id": "14fbfd46-2a98-4514-9ec0-4c6739221666", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/5"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 6.2}, "effectiveDateTime": "2025-07-11"}', 'internal', '2026-03-28 23:25:19.540685+00');
INSERT INTO public.fhir_resources VALUES (53, 5, 'Observation', '{"id": "e553e4ba-fcb4-4f1e-8296-2344c5a38b21", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/5"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 7.1}, "effectiveDateTime": "2025-10-09"}', 'internal', '2026-03-28 23:25:19.540685+00');
INSERT INTO public.fhir_resources VALUES (54, 5, 'Observation', '{"id": "ea9a36d7-428e-4a9c-9308-54225e77d03d", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/5"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 7.8}, "effectiveDateTime": "2026-01-07"}', 'internal', '2026-03-28 23:25:19.540685+00');
INSERT INTO public.fhir_resources VALUES (55, 5, 'Observation', '{"id": "bec63626-3403-4350-8e86-756846fe8025", "code": {"text": "HbA1c"}, "status": "final", "subject": {"reference": "Patient/5"}, "resourceType": "Observation", "valueQuantity": {"unit": "%", "value": 8.4}, "effectiveDateTime": "2026-04-07"}', 'internal', '2026-03-28 23:25:19.540686+00');
INSERT INTO public.fhir_resources VALUES (56, 5, 'MedicationStatement', '{"id": "b389790a-8f18-4256-a483-84b31cda0848", "status": "active", "subject": {"reference": "Patient/5"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-04-22", "medicationCodeableConcept": {"text": "Metformin"}}', 'internal', '2026-03-28 23:25:19.540686+00');
INSERT INTO public.fhir_resources VALUES (57, 5, 'MedicationStatement', '{"id": "9abec8bc-8de7-4e13-a899-846c6eabdbc3", "status": "active", "subject": {"reference": "Patient/5"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-06-21", "medicationCodeableConcept": {"text": "Jardiance"}}', 'internal', '2026-03-28 23:25:19.540687+00');
INSERT INTO public.fhir_resources VALUES (58, 5, 'MedicationStatement', '{"id": "28dc490e-9fcb-4e99-ac81-4f57f6948312", "status": "active", "subject": {"reference": "Patient/5"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-08-20", "medicationCodeableConcept": {"text": "Trulicity"}}', 'internal', '2026-03-28 23:25:19.540687+00');
INSERT INTO public.fhir_resources VALUES (59, 5, 'MedicationStatement', '{"id": "91574a2d-c94c-474b-9d85-1e40422a010f", "status": "active", "subject": {"reference": "Patient/5"}, "resourceType": "MedicationStatement", "effectiveDateTime": "2025-10-19", "medicationCodeableConcept": {"text": "Prednisone"}}', 'internal', '2026-03-28 23:25:19.540688+00');
INSERT INTO public.fhir_resources VALUES (60, 5, 'DocumentReference', '{"id": "4b1c2a86-7c0f-43df-ac92-50887e4d7a2c", "date": "2026-03-28T23:25:19.540233+00:00", "author": [{"display": "doctor1@clinic.com"}], "status": "current", "content": [{"attachment": {"data": "Sm9obiBQYXRlbCBkaWFiZXRlcyBmb2xsb3ctdXAgbm90ZS4gRW5jb3VyYWdlIGRpZXQgYWRoZXJlbmNlIGFuZCBleGVyY2lzZS4=", "contentType": "text/plain"}}], "subject": {"reference": "Patient/5"}, "description": "Clinical note", "resourceType": "DocumentReference"}', 'internal', '2026-03-28 23:25:19.540688+00');


--
-- Data for Name: patients; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.patients VALUES (7, 'Chris Walker', '1979-08-09', 'male', false, false, NULL, 'external', '2026-03-28 23:25:19.665054+00');
INSERT INTO public.patients VALUES (8, 'Nina Patel', '1991-05-21', 'female', false, false, NULL, 'external', '2026-03-28 23:25:19.785982+00');
INSERT INTO public.patients VALUES (9, 'Daniel Kim', '1984-12-03', 'male', false, false, NULL, 'external', '2026-03-28 23:25:19.90508+00');
INSERT INTO public.patients VALUES (6, 'Alex Morgan', '1988-02-14', 'female', false, false, NULL, 'external', '2026-03-28 23:25:19.545695+00');
INSERT INTO public.patients VALUES (1, 'George Burdell', '1978-04-12', 'male', true, true, 'internal', 'internal', '2026-03-28 23:25:18.937357+00');
INSERT INTO public.patients VALUES (2, 'Maria Lopez', '1985-07-23', 'female', true, true, 'internal', 'internal', '2026-03-28 23:25:19.055752+00');
INSERT INTO public.patients VALUES (3, 'David Chen', '1969-11-02', 'male', true, true, 'internal', 'internal', '2026-03-28 23:25:19.178217+00');
INSERT INTO public.patients VALUES (4, 'Sarah Kim', '1990-01-14', 'female', true, true, 'internal', 'internal', '2026-03-28 23:25:19.298382+00');
INSERT INTO public.patients VALUES (5, 'John Patel', '1975-09-30', 'male', true, true, 'internal', 'internal', '2026-03-28 23:25:19.41943+00');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.users VALUES (1, 'doctor1@clinic.com', 'pbkdf2:sha256:1000000$2SJurhEVir7P5BgD$83eaace44282df8a5f81a0731825947f999fa005dde8e2eb3dc87cd32c4a8c3f', 'clinician', NULL, '2026-03-28 23:25:18.817646+00');
INSERT INTO public.users VALUES (2, 'doctor2@clinic.com', 'pbkdf2:sha256:1000000$9518PN5MfeFhbGtp$6b7be10d7d054083b1e749178d29d0d53f6fab1d1e74415b589ce827a7511517', 'clinician', NULL, '2026-03-28 23:25:18.939071+00');
INSERT INTO public.users VALUES (3, 'george.burdell@patient.com', 'pbkdf2:sha256:1000000$M1MnSbzivzv5nW3Y$38bb250c33d9a682662bbf4fc6981749ceed558f9f2e06768e6280f3cda4baf0', 'patient', 1, '2026-03-28 23:25:19.061285+00');
INSERT INTO public.users VALUES (4, 'maria.lopez@patient.com', 'pbkdf2:sha256:1000000$FqXWwauPa3jd7G2A$b6460d40ca96ca4f401951d6256c9228ca64b5728b9351703605736364f3e7eb', 'patient', 2, '2026-03-28 23:25:19.181858+00');
INSERT INTO public.users VALUES (5, 'david.chen@patient.com', 'pbkdf2:sha256:1000000$PV1pql1QxGFwQK8m$8d31b61b7c2885374d0120e9e3d8ceb4d784a5425f3757b5a6a34b7d1cca9194', 'patient', 3, '2026-03-28 23:25:19.301453+00');
INSERT INTO public.users VALUES (6, 'sarah.kim@patient.com', 'pbkdf2:sha256:1000000$QXrR2NkqWsZcTAQo$e5a0e24b94c3f8c61bb168e6654645a72dbb057fd6bf564334224d23da45d127', 'patient', 4, '2026-03-28 23:25:19.423517+00');
INSERT INTO public.users VALUES (7, 'john.patel@patient.com', 'pbkdf2:sha256:1000000$6fh0piKXW15JvYEH$d1632956369f78bd4700a5f94c209fa201b708b315b447f144bd1b01ccdfdaa6', 'patient', 5, '2026-03-28 23:25:19.543435+00');
INSERT INTO public.users VALUES (8, 'alex.morgan@patient.com', 'pbkdf2:sha256:1000000$fjIgiMVyumSUsX5O$ea5623c71ab82561e4da154de658d11dfbd57afa7549b619a3059a6ebfb2e536', 'patient', 6, '2026-03-28 23:25:19.662494+00');
INSERT INTO public.users VALUES (9, 'chris.walker@patient.com', 'pbkdf2:sha256:1000000$RoS3S9mG8mR8mjS5$36ba6300df78ea48b405bb6e59636bd30e3ee509919fd6108600a7aec0fb9e99', 'patient', 7, '2026-03-28 23:25:19.782062+00');
INSERT INTO public.users VALUES (10, 'nina.patel@patient.com', 'pbkdf2:sha256:1000000$bpF0b2O44oCcQTR9$bb99487c3ae6e1e9a6ce44eaec88be7ccae116cd8312870c6e8b3f03268e794e', 'patient', 8, '2026-03-28 23:25:19.902243+00');
INSERT INTO public.users VALUES (11, 'daniel.kim@patient.com', 'pbkdf2:sha256:1000000$ShZWV66zdEgGsZdL$3c89a1e69887a0d63c51b64a800aeb643ef156684620bdc2ba82e8332e762cab', 'patient', 9, '2026-03-28 23:25:20.021017+00');


--
-- Name: fhir_resources_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.fhir_resources_id_seq', 80, true);


--
-- Name: patients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.patients_id_seq', 9, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 11, true);


--
-- Name: fhir_resources fhir_resources_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fhir_resources
    ADD CONSTRAINT fhir_resources_pkey PRIMARY KEY (id);


--
-- Name: patients patients_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_fhir_resources_resource_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_fhir_resources_resource_type ON public.fhir_resources USING btree (resource_type);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_role; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_role ON public.users USING btree (role);


--
-- Name: fhir_resources fhir_resources_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fhir_resources
    ADD CONSTRAINT fhir_resources_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: users users_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- PostgreSQL database dump complete
--

\unrestrict bh74ikf2mYE8StGZ12oUVlMLbiaTd79J1beV1seJfgg6ufRa0H8BOGt5YNdHI11

