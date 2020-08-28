
import app


def find_players(mid, first, last, player_keys=None):

    p_keys = player_keys or \
        'm_id fide_id expiry name city_prov rating rating_hi quick quick_hi'
    p_keys = p_keys.split()

    rsp = dict()
    with app.RATINGS_DB() as db:
        rsp['dbdate'] = app.dao.ratings.metadata.get_key(db, 'created')

        if mid:
            p = app.dao.ratings.player.get_mid(db, mid)
            p_iter = [p] if p else []
        else:
            p_iter = app.dao.ratings.player.getall_name(db, first, last)

        player_list = []
        for p in p_iter:
            p = {key: getattr(p, key) for key in p_keys}
            player_list.append(p)
        rsp['players'] = player_list

    return rsp


def get_player_details(mid, player_keys=None, tournament_keys=None, crosstable_keys=None):
    p_keys = player_keys or \
        'm_id fide_id expiry name city_prov rating rating_hi quick quick_hi tournaments'
    ct_keys = crosstable_keys or \
             't_id name last_day type score games_played rating_pre rating_perf rating_post rating_hi'
    p_keys = p_keys.split()
    ct_keys = ct_keys.split()

    rsp = dict()
    with app.RATINGS_DB() as db:
        rsp['dbdate'] = app.dao.ratings.metadata.get_key(db, 'created')

        player = app.dao.ratings.player.get_mid(db, mid)
        if not player:
            rsp['player'] = None
        else:
            app.dao.ratings.tournament.get_for_player(db, player)
            for i, t in enumerate(player.tournaments):
                new_t = {key: getattr(t, key) for key in ct_keys}
                player.tournaments[i] = new_t
            rsp['player'] = {key: getattr(player, key) for key in p_keys}

    return rsp


def get_tournament_crosstable(tid, tournament_keys=None, crosstable_keys=None):
    t_keys = tournament_keys or \
        't_id name last_day prov rounds pairings type org_m_id org_name crosstable'
    ct_keys = crosstable_keys or \
        'place m_id m_name games_played score results rating_pre rating_perf rating_post rating_hi'
    t_keys = t_keys.split()
    ct_keys = ct_keys.split()

    rsp = dict()
    with app.RATINGS_DB() as db:
        rsp['dbdate'] = app.dao.ratings.metadata.get_key(db, 'created')

        t = app.dao.ratings.tournament.get_tid(db, tid)
        if not t:
            rsp['tournament'] = None
        else:
            app.dao.ratings.tournament.get_crosstable_for_tournament(db, t)
            for i, ce in enumerate(t.crosstable):
                new_ce = {key: getattr(ce, key) for key in ct_keys}
                t.crosstable[i] = new_ce
            rsp['tournament'] = {key: getattr(t, key) for key in t_keys}

    return rsp
