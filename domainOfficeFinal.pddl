(define (domain office)
  (:requirements  :strips  :typing  :negative-preconditions  :disjunctive-preconditions )
  (:types
      buzzer1 buzzer2 person1 person2 room fan light message  - object
   )
   
    (:predicates
         
          (employee-allowed)
          (employee-denied)
          (comfortable-temp)
          (light-sufficient)
         
          (motion ?p1 - person1)
          (on ?b1 - buzzer1)
          (off ?b1 - buzzer1)
         
          (bodytemp ?p2 - person2)
          (on0 ?b2 - buzzer2)
          (off0 ?b2 - buzzer2)
         
          (on1 ?l - light)
          (off1 ?l - light)
         
          (on2 ?f - fan)
          (off2 ?f - fan)
         
         

          (at-buzzer1 ?b1 - buzzer1 ?p1 - person1)
          (at-buzzer2 ?b2 - buzzer2 ?p2 - person2)
         
          (at-light ?l - light ?r - room)
          (at-fan ?f - fan ?r - room)
         
   
          (send ?m - message)
         

   )

   (:functions
     
     
 (buzzer1 ?b1 - person1)
 (buzzer2 ?b2 - person2)
 (temp ?r - room)
 (light ?r - room)
 (bodytemp?p2 - person2)
 (humidity ?r - room)
 (bodytemp_limit)
 (temp_limit)
 (light_limit)
 (humidity_limit)
   )
   
   
   
 
 (:action switchoff_buzzer1
        :parameters (?b1 - buzzer1 ?p1 - person1 ?m - message)
        :precondition (and (on ?b1) (motion ?p1))
        :effect (and(not(on ?b1)) (send ?m) (employee-allowed))
   )
   
   (:action switchon_buzzer1
        :parameters (?b1 - buzzer1 ?p1 - person1 ?m - message)
        :precondition (or (not(on ?b1)) (motion ?p1 ))
        :effect (and (on ?b1) (send ?m) (employee-allowed))
   )
   
   (:action switchoff_buzzer2
 
        :parameters (?b2 - buzzer2 ?p2 - person2 ?m - message)
        :precondition (and (on0 ?b2) (<(bodytemp ?p2) (bodytemp_limit)))
       
        :effect (and(not(on0 ?b2)) (send ?m) (employee-denied ))
   )
   
   (:action switchon_buzzer2
        :parameters (?b2 - buzzer2 ?p2 - person2 ?m - message)
        :precondition (or (not(on0 ?b2)) (>(bodytemp ?p2) (bodytemp_limit)))
        :effect (and (on0 ?b2) (send ?m) (employee-denied))
   )
   
   (:action switchoff_light
        :parameters (?l - light ?r - room ?m - message)
        :precondition (and (on1 ?l) (>(light ?r) (light_limit)))
        :effect (and(not(on1 ?l)) (send ?m) (light-sufficient))
   )
   
   (:action switchon_light
        :parameters (?l - light ?r - room ?m - message)
        :precondition (or (not(on1 ?l)) (<(light ?r) (light_limit)))
        :effect (and (on1 ?l) (send ?m) (light-sufficient))
   )
   

       
   (:action switchoff_fan
        :parameters (?f - fan ?r - room ?m - message)
        :precondition (and (on2 ?f) (>(temp ?r) (temp_limit)) (>(humidity ?r) (humidity_limit)))
        :effect (and(not(on2 ?f)) (send ?m) (comfortable-temp))
   )
   
   (:action switchon_fan
        :parameters (?f - fan ?r - room ?m - message)
        :precondition (or (not(on2 ?f)) (<(temp ?r) (temp_limit)) (<(humidity ?r) (humidity_limit)))
        :effect (and (on2 ?f) (send ?m) (comfortable-temp))
   )
   
   
   )

