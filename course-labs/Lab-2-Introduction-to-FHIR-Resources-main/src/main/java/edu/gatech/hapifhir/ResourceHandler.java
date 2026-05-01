package edu.gatech.hapifhir;

import org.hl7.fhir.instance.model.api.IBaseResource;
import org.hl7.fhir.r4.model.CodeableConcept;
import org.hl7.fhir.r4.model.Coding;
import org.hl7.fhir.r4.model.Extension;
import org.hl7.fhir.r4.model.HumanName;
import org.hl7.fhir.r4.model.Identifier;
import org.hl7.fhir.r4.model.Patient;

import org.hl7.fhir.r4.model.Observation;
import org.hl7.fhir.r4.model.StringType;

import java.util.ArrayList;
import java.util.LinkedList;


public class ResourceHandler {

    public ResourceHandler() {
        // Do not add anything to this constructor method.
    }

    public String getId(IBaseResource resource){
        String id = "";
        // Get the "id" value of any resource without any additional data. (No base server urls, resource types, etc.)
        // START STUDENT CODE HERE

        if (resource != null && resource.getIdElement() != null) {
            String part = resource.getIdElement().getIdPart();
            if (part != null) id = part;
        }

        // END STUDENT CODE HERE

        return id; // Replace this. Returns empty string just so it will compile.
    }

    public Observation addObservationCode(Observation observation, String system, String code, String display){
        // Create a CodeableConcept and add it to an existing Observation resource.
        // START STUDENT CODE HERE

        if (observation == null) return null;
        CodeableConcept cc = new CodeableConcept();
        cc.addCoding(new Coding(system, code, display));
        observation.setCode(cc);

        // END STUDENT CODE HERE
        return observation;
    }

    public Patient updateOfficialGivenName(Patient patient, String givenName){
        // Being given a Patient resource and a given name string, set (not add) the name to the HumanName object in the
        // Patient's list of names with a use of "official". No other values should be modified.
        // Note: There is only one HumanName with use set to official, you do not need to handle multiple official
        // names. The name provided should be the only given name (a single item List).

        // START STUDENT CODE HERE

        if (patient == null) return null;
        if (givenName == null) return patient;

        for (HumanName hn : patient.getName()) {
            if (hn != null && hn.getUse() != null && "official".equalsIgnoreCase(hn.getUse().toCode())) {
                ArrayList<StringType> given = new ArrayList<>();
                given.add(new StringType(givenName));
                hn.setGiven(given);
                break;
            }
        }

        // END STUDENT CODE HERE
        return patient;
    }

    public Patient createUSCorePatient(String id, Identifier identifier, HumanName name, Coding ethnicityOmbCoding, Coding ethnicityDetailedCoding, String ethnicityText){
        Patient usCorePatient = new Patient(); // Use this Patient object.

        // Create a US Core Patient (a Patient resource using the US Core profile) with name, identifier, ethnicity, and
        // any required profile meta information. For name you are provided a HumanName object and for Identifier you
        // are provided with an Identifier object. These should be simple to handle. Ethnicity you are provided with
        // individual portions of the extension, the OMB category coding, Detailed ethnicity coding, and Text
        // representation as a String. You are responsible for setting these coding elements in the correct location
        // within the extension along with setting the metadata for each portion (the URLs).
        //
        // http://hl7.org/fhir/us/core/StructureDefinition-us-core-patient.html
        // http://hl7.org/fhir/us/core/StructureDefinition-us-core-ethnicity.html
        //
        // START STUDENT CODE HERE

        // set id if provided
        if (id != null && !id.isEmpty()) {
            usCorePatient.setId(id);
        }

        // add identifier if provided
        if (identifier != null) {
            usCorePatient.addIdentifier(identifier);
        }

        // add name if provided
        if (name != null) {
            usCorePatient.addName(name);
        }

        // add US Core profile metadata to meta
        usCorePatient.getMeta().addProfile("http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient");

        // build ethnicity extension per US Core ethnicity structure
        if (ethnicityOmbCoding != null || ethnicityDetailedCoding != null || (ethnicityText != null && !ethnicityText.isEmpty())) {
            Extension ethnicityExt = new Extension("http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity");

            if (ethnicityOmbCoding != null) {
                ethnicityExt.addExtension(new Extension("ombCategory", ethnicityOmbCoding));
            }
            if (ethnicityDetailedCoding != null) {
                ethnicityExt.addExtension(new Extension("detailed", ethnicityDetailedCoding));
            }
            if (ethnicityText != null && !ethnicityText.isEmpty()) {
                ethnicityExt.addExtension(new Extension("text", new StringType(ethnicityText)));
            }

            usCorePatient.addExtension(ethnicityExt);
        }

        // END STUDENT CODE HERE
        return usCorePatient;
    }
}
