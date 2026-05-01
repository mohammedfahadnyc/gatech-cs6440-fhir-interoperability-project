package edu.gatech.hapifhir;

import org.hl7.fhir.r4.model.Bundle;
import org.hl7.fhir.r4.model.Patient;

import java.util.ArrayList;

public class BundleHandler {

    public BundleHandler() { }

    public String navigateBundle(Bundle bundle, String link) {

        // START STUDENT CODE HERE
        if (bundle == null || link == null) return "-1";

        for (Bundle.BundleLinkComponent lc : bundle.getLink()) {
            if (lc == null) continue;
            String rel = lc.getRelation();
            if (rel != null && rel.equals(link)) {
                String url = lc.getUrl();
                return url == null ? "-1" : url;
            }
        }
        // END STUDENT CODE HERE

        return "-1";
    }

    public ArrayList<Patient> getListOfDeceasedPatients(Bundle bundle) {
        ArrayList<Patient> patientArrayList = new ArrayList<>();

        // START STUDENT CODE HERE
        if (bundle == null) return patientArrayList;

        for (Bundle.BundleEntryComponent entry : bundle.getEntry()) {
            if (entry == null || entry.getResource() == null) continue;
            if (entry.getResource() instanceof Patient) {
                Patient p = (Patient) entry.getResource();
                boolean deceased = false;


                try {
                    if (p.hasDeceasedBooleanType() && p.getDeceasedBooleanType() != null
                            && p.getDeceasedBooleanType().getValue() != null) {
                        deceased = p.getDeceasedBooleanType().getValue();
                    }
                } catch (Exception ignored) { }

                // If a deceased DateTime is present, treat as deceased
                if (!deceased && p.hasDeceasedDateTimeType()) {
                    deceased = true;
                }

                if (deceased) patientArrayList.add(p);
            }
        }
        // END STUDENT CODE HERE

        return patientArrayList;
    }
}
