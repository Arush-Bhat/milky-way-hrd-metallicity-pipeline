SELECT
    d.targetid, d.z, m.param,
    g.source_id, g.parallax, g.phot_g_mean_mag, g.phot_bp_mean_mag, g.phot_rp_mean_mag
FROM
    desi_dr1.zpix AS d
JOIN
    desi_dr1.mws AS m ON d.targetid = m.targetid
JOIN
    gaia_dr3.gaia_source AS g ON m.source_id = g.source_id
WHERE
    g.parallax_over_error > 5.0
    AND g.phot_bp_rp_excess_factor < 1.3
