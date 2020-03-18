
import regex

class DrugAnnotator:
    # modified DrugNLP to work per mention not per discharge summary
    # target doc is Clinical Note - does not check the ". . STOP" pattern sometimes seen in a discharge summary drug list
    def __init__(self, all_drugs):
        # all_drugs is a list of drug names
        #used to check size of detectied drug lists
        #these values are specifically tuned to our records
        self.empty_list_size = 550 #this is tuned specifically to our records
        self.multicomp_aid = 300
        self.negation_window = 20
        self.review_window = 30
        
        #build regex
        self.edge_cases = ["DRUGS ON XXXXXXXXX", "XXXXX ON DISCHARGE", "DRUGS XXXXXXXXXXXX", "DRUGS ON X"]
        self.all_drugs = all_drugs
        self.positive_regex = {}
        for dr in self.all_drugs:
            term = dr.upper()
            pattern = "(?:"+term+"){s<=1}"
            self.positive_regex[dr] = regex.compile(pattern) # can only have one way to find each drug
            
        self.negative_regex = {}
        for dr in self.all_drugs:
            term = dr.upper()
            pattern = term + r" (?:STOP|WITHH|WAS WITHH|DISCONTINUE|TO BE STOPPED|HAS BEEN STOPPED|WAS STOPPED|CHANGED TO|SWITCHED TO)"
            self.negative_regex[dr] = [regex.compile(pattern)]
            pattern = r"(?:STOP|STOPPED|STOPPED HIS|STOPPED HER|WITHHOLD|WITHHELD|DISCONTINUE|DISCONTINUED|NOT ON|NOT CURRENTLY ON|CONSIDER|CONSIDER RESTARTING) " + term
            self.negative_regex[dr].append(regex.compile(pattern))
            #allergies - considered negation as not a positive mention
            pattern = r"(?:ALELRGIC|ALLERGIC TO|ALLERGIES) " + term
            self.negative_regex[dr].append(regex.compile(pattern))
        
        #allow 2 substitutions here for S and D
        self.drugs_on_disch_regex = regex.compile('(?:DRUGS ON DISCHARGE){s<=2}')
        self.discharge_medication_regex = regex.compile('(?:DISCHARGE MEDICATION){s<=2}')
        self.drug_list_end_regex = []
        #self.drug_list_end_regex.append(regex.compile('(?:DRUG LIST COMPLETED){s<=2}'))
        #self.drug_list_end_regex.append(regex.compile('(?:TTA COMPLETED){s<=2}'))
        self.drug_list_end_regex.append(regex.compile('(?:FINAL TTA ASSEMBLY){s<=2}'))
        #expression for a specific negation possible in discharge drug list

        
    def annotate(self, doc):
        doc = doc.upper().replace('\r\n','\n')
        
        #negation detection works better with newlines removed
        doc = doc.replace('\n',' ')
        doc = doc.replace('\r',' ')
        doc = regex.sub(r'  +',' ', doc)
        doc = doc.replace(" .", ".")
        doc = regex.sub(r'\.+', ".", doc)
        
        doc_data = {'mentions': []}
            
        for dr in self.all_drugs:
            #{'mentioned':False, 'negated':False, 'status': False}
            reg = self.positive_regex[dr]
            m = regex.finditer(reg.pattern, doc)
            for match in m:
                # each time the drug name is found, test for negation
                mention = {'drug': dr, 'mentioned':True, 'negated':False}
                # get context and search within it for negation
                ctx_from = max(match.span()[0] - self.review_window, 0)
                ctx_to = min(match.span()[1] + self.review_window, len(doc))
                ctx = doc[ctx_from : ctx_to]
                mention['ctx'] = ctx
                mention['start'] = match.span()[0]
                mention['end'] = match.span()[1]

                ctx_from = max(match.span()[0] - self.negation_window, 0)
                ctx_to = min(match.span()[1] + self.negation_window, len(doc))
                ctx = doc[ctx_from : ctx_to]

                for negator in self.negative_regex[dr]:
                    if len(negator.findall(ctx)) > 0:
                        mention['negated'] = True
                doc_data['mentions'].append(mention)

        return doc_data
         
    
                
        
