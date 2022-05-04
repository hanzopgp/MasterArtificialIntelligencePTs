(defrule my_init
	 (initial-fact)
=>
	(watch facts)
	(watch rules)

	(assert (a_tache patient))
	(assert (a_bouton patient peu))
	(assert (a_froid patient))
	(assert (a_fievre patient fort))
	(assert (a_mal_aux_yeux patient))
	(assert (a_amygdales_rouge patient))
	(assert (a_peau patient pele))
	(assert (a_peau patient seche))
)

(defrule a_eruption_cutanee
	(a_bouton ?p ?x)
=>	(assert (a_eruption_cutanee ?p))
)

(defrule a_exantheme
	(a_eruption_cutanee ?p)
	(a_tache ?p)
=>	(assert (a_exantheme ?p))
)

(defrule est_febrile1
	(a_fievre ?p fort)
=>	(assert (est_febrile ?p))
)

(defrule est_febrile2
	(a_froid ?p oui)
=>	(assert (est_febrile ?p))
)

(defrule est_suspect
	(a_amygdales_rouge ?p)
	(a_tache ?p)
	(a_peau ?p pele)
=>	(assert (est_suspect ?p))
)

(defrule a_rougeole1
	(est_febrile ?p)
	(a_mal_aux_yeux ?p)
	(a_exantheme ?p)
=>	(assert (a_rougeole ?p oui))
)

(defrule a_rougeole2
	(est_suspect ?p)
	(a_fievre ?p fort)
=>	(assert (a_rougeole ?p oui))
)

(defrule a_pas_rougeole1
	?f <- (a_rougeole ?p oui)
	(a_fievre ?p faible)
	(a_bouton ?p peu)
=>	(assert (a_rougeole ?p non))
	(retract ?f)
)

(defrule a_pas_rougeole2
	(a_fievre ?p faible)
	(a_bouton ?p peu)
=>	(assert (a_rougeole ?p non))
)

(defrule a_douleur1
	(a_mal_aux_yeux ?p)
=>	(assert (a_douleur ?p))
)

(defrule a_douleur2
	(a_mal_au_dos ?p)
=>	(assert (a_douleur ?p))
)

(defrule a_grippe
	(a_mal_au_dos ?p)
	(est_febrile ?p)
=>	(assert (a_grippe ?p))
)

(defrule a_varicelle
	(a_rougeole ?p non)
	(a_demangeaisons ?p fort)
	(a_pustules ?p oui)
=>	(assert (a_varicelle ?p oui))
)

(defrule a_rubeole
	(a_rougeole ?p non)
	(a_peau ?p seche)
	(a_inflammation_ganglions ?p)
	(a_froid ?p non)
=>	(assert (a_rubeole ?p oui))
)

; Strategie

; CLIPS effectue le chainage avant

; L'ordre d'execution
;==> f-1     (a_tache patient)
;==> f-2     (a_bouton patient peu)
;==> f-3     (a_froid patient)
;==> f-4     (a_fievre patient fort)
;==> f-5     (a_mal_aux_yeux patient)
;==> f-6     (a_amygdales_rouge patient)
;==> f-7     (a_peau patient pele)
;==> f-8     (a_peau patient seche)
;FIRE    2 est_suspect: f-6,f-1,f-7
;==> f-9     (est_suspect patient)
;FIRE    3 a_rougeole2: f-9,f-4
;==> f-10    (a_rougeole patient oui)
;FIRE    4 a_douleur1: f-5
;==> f-11    (a_douleur patient)
;FIRE    5 est_febrile1: f-4
;==> f-12    (est_febrile patient)
;FIRE    6 a_eruption_cutanee: f-2
;==> f-13    (a_eruption_cutanee patient)
;FIRE    7 a_exantheme: f-13,f-1
;==> f-14    (a_exantheme patient)
;FIRE    8 a_rougeole1: f-12,f-5,f-14

; Le patient est diagnotisque la rougeole
