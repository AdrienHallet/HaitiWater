CREATE OR REPLACE VIEW public.water_network_virtualelementtotal AS
 SELECT e.id AS relevant_model,
    ( SELECT COALESCE(sum(c.household_size + 1), 0::bigint) AS "coalesce"
           FROM consumers_consumer c
          WHERE c.water_outlet_id = e.id) AS total_consumers,
    ( SELECT COALESCE(sum(r.quantity_distributed), 0::double precision) AS "coalesce"
           FROM report_report r
          WHERE r.water_outlet_id = e.id AND r.was_active) AS total_distributed
   FROM water_network_element e
  GROUP BY e.id;