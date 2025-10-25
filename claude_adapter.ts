export async function suggestEdits(notes:string, metrics:any){
  // TODO: call Anthropic Claude and return strict JSON
  return { action:'edit', targets:['image'], params:{ filter:'cinematic1' }, rationale:'stub', next_tests:['brighter first frame'] };
}