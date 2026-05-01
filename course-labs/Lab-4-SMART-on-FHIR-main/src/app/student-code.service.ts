import { Injectable } from '@angular/core';
import { Observable, from, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StudentCodeService {

  constructor() {}

  // This is given as an example of the client, do not modify it.
  example_searchObservations(client, loincCode): Observable<any> {
    let queryParams = new URLSearchParams();
    queryParams.set('patient', client.patient.id);
    queryParams.set('code', loincCode);
    queryParams.set('_sort', '-date');
    return from<any[]>(client.request("Observation?" + queryParams, {flat: true}))
  }

  exercise_0_testScopes(): string {
    return 'launch profile openid online_access patient/Patient.read patient/Observation.read patient/MedicationRequest.*'
  }



  exercise_1_searchMedicationRequests(client): Observable<any> {
    let queryParams = new URLSearchParams();
    queryParams.set('patient', client.patient.id);
    return from<any[]>(client.request("MedicationRequest?" + queryParams, {flat: true}));
  }

  exercise_2_updateMedicationRequest(client, resource: any, status: string): Observable<any> {
    resource.status = status;
    return from<any[]>(client.update(resource));
  }

  exercise_3_createMedicationRequest(client, medicationName: string): Observable<any> {
    let newResource = {
      resourceType: "MedicationRequest",
      status: "draft",
      intent: "order",
      subject: {
        reference: "Patient/" + client.patient.id
      },
      medicationCodeableConcept: {
        text: medicationName
      }
    };

    return from<any[]>(client.create(newResource));
  }
}
