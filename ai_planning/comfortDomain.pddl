(define (domain office)
  (:requirements   :strips  :typing  :negative-preconditions :disjunctive-preconditions :fluents :equality :conditional-effects)
  (:types
   room light person fan humidifier message  - object
   )
   
    (:predicates
          
          (comfortable-temperature)
          (brightness-sufficient)
          (comfortable-humidity)
          (off ?l - light)
          (off1 ?f - fan)
          (off2 ?h - humidifier)
          (at-light ?l - light  ?r - room ?p - person)
          (at-fan ?f - fan ?r - room ?p - person)
          (at-humidifier ?h - humidifier ?r - room ?p - person)
          (send ?m - message)     
    )

   (:functions
    
	  (temp ?r - room )
	  (lightintensity ?r - room)
	  (humidity ?r - room)
	  (temp_limit)
	  (temp1_limit)
	  (humidity_limit)
      (lightintensity_limit)

   )
	  
  
  ; automatic brightness control in the office

   (:action switchoff_light
        :parameters (?l - light ?r - room ?p - person ?m - message)
        :precondition (and (off ?l) (<(lightintensity ?r) (lightintensity_limit)))
        :effect (and (not(off ?l)) (send ?m) (brightness-sufficient))
    )

    (:action switchon_light
        :parameters (?l - light ?r - room ?p - person ?m - message)
        :precondition (or (not(off ?l)) (>=(lightintensity ?r) (lightintensity_limit)))
        :effect (and (off ?l) (send ?m) (brightness-sufficient))
    )
   
   
   
   ; automatic ventilator control in the office

   (:action switchoff_fan
        :parameters (?f - fan ?r - room ?p - person ?m - message)
        :precondition (and (off1 ?f) (<(temp ?r) (temp_limit)))
        :effect (and(not(off1 ?f)) (send ?m) (comfortable-temperature))
   )
   
   (:action switchon_fan
        :parameters (?f - fan ?r - room ?p - person ?m - message)
        :precondition (or (not(off1 ?f)) (>(temp ?r) (temp1_limit)))
        :effect (and (off1 ?f) (send ?m) (comfortable-temperature))
   )
   


   ; automatic humidifer valve control in the office

    (:action switchoff_humidifier
        :parameters (?h - humidifier ?r - room ?p - person ?m - message)
        :precondition (and (off2 ?h) (>(humidity ?r) (humidity_limit)))
        :effect (and(not(off2 ?h)) (send ?m) (comfortable-humidity))
     )
   
    (:action switchon_humidifier
        :parameters (?h - humidifier ?r - room ?p - person ?m - message)
        :precondition (or (not(off2 ?h)) (<(humidity ?r) (humidity_limit)))
        :effect (and (off2 ?h) (send ?m) (comfortable-humidity))
     )
   
)
