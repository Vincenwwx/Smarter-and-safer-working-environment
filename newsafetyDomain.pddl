(define (domain office)
  (:requirements   :strips  :typing  :negative-preconditions :disjunctive-preconditions :fluents :equality :conditional-effects)
  (:types
   buzzer buzzer1 greenled redled person message  - object
   )
   
    (:predicates
         
          (bodytempcheck-performed)
          (employee-detected)
          (off3 ?b - buzzer ) 
          (off5 ?g - greenled)
          (off4 ?b1 - buzzer1) 
          (off6 ?r - redled)
          (at-buzzer ?b - buzzer ?p - person)
          (at-buzzer1 ?b1 - buzzer1 ?p - person)
          (at-greenled ?g - greenled ?p - person)
           (at-redled ?r - redled ?p - person)
          (send ?m - message)     
    )

   (:functions
    
	  
	  (bodytemp ?p - person)
	  (motion ?p - person)
	  (bodytemp_limit)
	  (motion_value)
   )
   

   
     ;ir sesnsor to detect person movement
   
         ;buzzer1 (off) says 'nothing'
    (:action switchoff_buzzer1 
        :parameters (?b1 - buzzer1 ?p - person ?m - message)
        :precondition (and (off4 ?b1) (<(motion ?p) (motion_value))) 
        :effect (and(not(off4 ?b1)) (send ?m) (employee-detected))
     )
        ;buzzer1 (on) must say 'please proceed to temperature check'
     (:action switchon_buzzer1 
        :parameters (?b1 - buzzer1 ?p - person ?m - message)
        :precondition (or (not(off4 ?b1)) (>=(motion ?p) (motion_value)))
        :effect (and (off4 ?b1) (send ?m) (employee-detected))
      )    
   
      ; automatic bodytemp check in front of the office

      ; person detected & body temp in allowable limit 'greenled on' and buzzer must say 'Please come in'

    (:action switchon_greenled_buzzer
        :parameters ( ?b - buzzer ?g - greenled ?p - person ?m - message)
        :precondition (and (off3 ?b) (off5 ?g) (>=(motion ?p) (motion_value)) (<(bodytemp ?p) (bodytemp_limit))) 
        :effect (and (not(off3 ?b)) (not(off5 ?g)) (send ?m) (bodytempcheck-performed))
     )
      
   
       ; person detected & body temp not in allowable limit 'redled on' and buzzer mut say 'Sorry, abnormal temperature'


     (:action switchon_redled_buzzer
        :parameters (?b - buzzer ?r - redled ?p - person ?m - message)
        :precondition (and (off3 ?b) (off6 ?r) (>=(motion ?p) (motion_value)) (>(bodytemp ?p) (bodytemp_limit)))
        :effect (and (not(off3 ?b)) (not(off6 ?r)) (send ?m) (bodytempcheck-performed))
     )    

     (:action switchoff_greenled_redled_buzzer
        :parameters (?b - buzzer ?r - redled ?g - greenled ?p - person ?m - message)
        :precondition (or (not(off3 ?b)) (not(off5 ?g)) (not(off6 ?r)) (<(motion ?p) (motion_value)))
        :effect (and (off3 ?b) (off5 ?g) (off6 ?r) (send ?m) (bodytempcheck-performed))
     )  
   )

  
     
   
  
   
     

