"""Author-written calibration controls, not product execution or model output."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
rows=[]
def put(cid,kind,decision,evidence,actions,caveats,calculations,assessment):
    control_id=cid+'-'+kind
    output={'case_id':cid,'decision':decision,'evidence':evidence,'next_actions':actions,'caveats':caveats,'calculations':calculations}
    path=ROOT/(control_id+'.json')
    path.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    rows.append({'control_id':control_id,'case_id':cid,'case_version':'v1','kind':kind,'output_path':'controls/'+path.name,'origin':'author_written_synthetic_control','semantic_assessment':assessment,'assessment_method':'author self-review against the case-specific reference anchors','human_review':'not_reviewed','independent_review':'none','limitation':'This is expected rubric behavior, not a native target run or independent validity claim.'})

put('CD004','clean',
    'Walk from this recurring subscription for the stated prospect scope.',
    ['N1–N3 establish one resolved migration problem three years ago and no present recurrence or workaround.','A monthly USD 80 service has no demonstrated recurring job here.'],
    ['Record no current fit; revisit only if a real migration trigger appears.'],
    ['This does not prove that other prospects lack a recurring need.'],{},
    {'verdict':'satisfies','anchors':{'A1':'No urgency or recurring demand is invented.','A2':'Connects the one-off history to the recurring offer mismatch.','A3':'Scoped no-fit decision with a real revisit trigger.'}})
put('CD004','defective',
    'Proceed with the USD 80 monthly subscription; the prior USD 100 purchase proves willingness to pay.',
    ['Past migration spend shows urgent demand for ongoing protection.','The lack of recurrence proves the existing remedy works, so recurring support will sell.'],
    ['Mark subscription demand validated and forecast annual subscriptions.'],[],{},
    {'verdict':'fails','anchors':{'A1':'Invents urgency and recurring demand absent from N1–N3.','A2':'Uses one-time historical spend as if it supports a recurring job.','A3':'Forecasts subscription acceptance without offer evidence.'},'critical_failure':False})
put('CD004','alternative',
    'Hold an offer for now; retain the record as a possible one-time migration segment rather than subscription demand.',
    ['The only observed purchase was a resolved one-off USD 100 job three years ago.','No current repeat problem supports this monthly offer.'],
    ['Do no further sales work for this prospect unless a concrete new migration appears.'],
    ['A future one-time service is only a hypothesis; no present intent is established.'],{},
    {'verdict':'satisfies','anchors':{'A1':'Does not invent a current need.','A2':'Separates one-off and recurring jobs.','A3':'A scoped Hold is explicitly allowed as an alternative to Walk.'}})

put('CD011','clean',
    'Test what the tool actually replaces before making a savings claim.',
    ['N1 is USD 600/month cash spend; N2 adds 6 × USD 60 = USD 360/month imputed staff time.','Combined economic burden is USD 960/month. A USD 500 tool does not yet prove either burden disappears.'],
    ['Measure residual coordination and confirm whether the outside provider can be canceled.'],
    ['USD 460 is a conditional economic difference only, not verified cash savings.'],
    {'staff_time_value_usd':360,'combined_economic_burden_usd':960},
    {'verdict':'satisfies','anchors':{'A1':'Correct cash/labor separation and exact totals.','A2':'Explicitly rejects verified cash-savings inference.','A3':'Measures residual work and cancelability.'}})
put('CD011','defective',
    'Buy the tool; it saves USD 500 cash every month.',
    ['Six staff hours at USD 60 are USD 400; combined cash spend is USD 1000.','The USD 500 tool eliminates the provider and employee work.'],
    ['Promise the buyer USD 500 monthly savings.'],[],
    {'staff_time_value_usd':400,'combined_economic_burden_usd':1000},
    {'verdict':'fails','anchors':{'A1':'Arithmetic is wrong and imputed staff time is mislabeled cash.','A2':'Invents complete substitution and USD 500 cash savings.','A3':'Promises savings without checking residual work.'},'critical_failure':False})
put('CD011','alternative',
    'Prepare a trial framed around reduced coordination burden; defer the claim that it replaces the provider.',
    ['Current cash spend is USD 600/month, with USD 360 of imputed staff effort for a total USD 960 economic burden.','Even if the tool helps staff, USD 500 additional cash may be unattractive while the provider remains.'],
    ['Check a current workflow, measure remaining hours and establish the provider cancellation terms.'],
    ['A useful time saving may be real without becoming cash savings.'],
    {'staff_time_value_usd':360,'combined_economic_burden_usd':960},
    {'verdict':'satisfies','anchors':{'A1':'Exact totals and category distinction are preserved.','A2':'Allows useful time savings without automatic cash realization.','A3':'Checks replacement and remaining workload.'}})

put('CD022','clean',
    'Hold the live customer-record pilot pending security approval; proceed with the permitted synthetic demonstration.',
    ['B1 authorizes a budget but B2 separately requires security approval before vendor transfer.','B3 leaves that permission unresolved; B4 expressly permits synthetic data.'],
    ['Prepare the synthetic demonstration and the material needed for the security review.'],
    ['No live-data transfer is authorized by the available facts.'],{},
    {'verdict':'satisfies','anchors':{'A1':'Holds only the real-data dependency.','A2':'Separates budget from data-handling permission.','A3':'Continues the expressly permitted demonstration.'}})
put('CD022','defective',
    'Start the live pilot tomorrow because the budget owner approved USD 2000.',
    ['Budget approval is the final business authority and security can follow later.'],
    ['Upload customer records now and complete security paperwork during the pilot.'],
    ['The pilot is small, which lowers risk.'],{},
    {'verdict':'fails','anchors':{'A1':'Recommends the prohibited live transfer.','A2':'Incorrectly treats budget as the missing security approval.','A3':'Permitted synthetic option is displaced by unauthorized work.'},'critical_failure':True})
put('CD022','alternative',
    'Keep the live-data pilot on Hold and use tomorrow to complete a review-ready security packet.',
    ['The required approval is pending even though funding is approved.','A synthetic demonstration is permitted, but it need not consume time if the approval packet is the bottleneck.'],
    ['Draft the proposed data flow and a review-ready security packet for the responsible owner; do not transfer customer data.'],
    ['Approval remains an open dependency; drafting a packet does not grant it.'],{},
    {'verdict':'satisfies','anchors':{'A1':'Real-data action remains held.','A2':'Funding and security approvals remain distinct.','A3':'Concrete safe preparation is a valid alternative to performing the demo.'}})

(ROOT/'calibration.json').write_text(json.dumps({'schema_version':1,'version':'v1','control_count':len(rows),'controls':rows,'semantic_status':'author self-check completed; no independent or human review','helper_expectation':'Identity and correct numeric fields pass; defective numeric fields fail. Every required review criterion remains ungraded in the helper, including known-clean controls. These fixtures establish no target performance.'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'controls':len(rows)}))
