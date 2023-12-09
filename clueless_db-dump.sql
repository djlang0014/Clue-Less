--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locations (
    location_name character varying NOT NULL,
    is_restricted boolean DEFAULT false
);


ALTER TABLE public.locations OWNER TO postgres;

--
-- Name: board_locations_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.board_locations_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.board_locations_location_id_seq OWNER TO postgres;

--
-- Name: board_locations_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.board_locations_location_id_seq OWNED BY public.locations.location_name;


--
-- Name: game_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game_session (
    session_id character varying NOT NULL,
    is_active boolean NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone,
    num_players integer,
<<<<<<< Updated upstream
    case_file integer[],
=======
    case_file character varying[],
>>>>>>> Stashed changes
    player_won character varying
);


ALTER TABLE public.game_session OWNER TO postgres;

--
-- Name: game_info_game_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.game_info_game_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.game_info_game_id_seq OWNER TO postgres;

--
-- Name: game_info_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_info_game_id_seq OWNED BY public.game_session.session_id;


--
-- Name: game_states; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game_states (
    state_id integer NOT NULL,
    game_id character varying,
    "timestamp" timestamp without time zone NOT NULL,
    current_player character varying,
    game_data jsonb
);


ALTER TABLE public.game_states OWNER TO postgres;

--
-- Name: game_states_state_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.game_states_state_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.game_states_state_id_seq OWNER TO postgres;

--
-- Name: game_states_state_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_states_state_id_seq OWNED BY public.game_states.state_id;


--
-- Name: player_location_map; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.player_location_map (
    map_id integer NOT NULL,
    player_id character varying NOT NULL,
    location_name character varying,
    session_id character varying
);


ALTER TABLE public.player_location_map OWNER TO postgres;

--
-- Name: player_location_map_map_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.player_location_map_map_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.player_location_map_map_id_seq OWNER TO postgres;

--
-- Name: player_location_map_map_id_seq1; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.player_location_map_map_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.player_location_map_map_id_seq1 OWNER TO postgres;

--
-- Name: player_location_map_map_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.player_location_map_map_id_seq1 OWNED BY public.player_location_map.map_id;


--
-- Name: players; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.players (
    player_id character varying NOT NULL,
    player_name character varying(50) NOT NULL,
    character_name character varying(50) NOT NULL,
    session_id character varying
);


ALTER TABLE public.players OWNER TO postgres;

--
-- Name: players_player_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.players_player_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.players_player_id_seq OWNER TO postgres;

--
-- Name: players_player_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.players_player_id_seq OWNED BY public.players.player_id;


--
-- Name: game_session session_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_session ALTER COLUMN session_id SET DEFAULT nextval('public.game_info_game_id_seq'::regclass);


--
-- Name: game_states state_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_states ALTER COLUMN state_id SET DEFAULT nextval('public.game_states_state_id_seq'::regclass);


--
-- Name: locations location_name; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations ALTER COLUMN location_name SET DEFAULT nextval('public.board_locations_location_id_seq'::regclass);


--
-- Name: player_location_map map_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.player_location_map ALTER COLUMN map_id SET DEFAULT nextval('public.player_location_map_map_id_seq1'::regclass);


--
-- Name: players player_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.players ALTER COLUMN player_id SET DEFAULT nextval('public.players_player_id_seq'::regclass);


--
-- Data for Name: game_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game_session (session_id, is_active, start_time, end_time, num_players, case_file, player_won) FROM stdin;
<<<<<<< Updated upstream
=======
mi1tdz	t	2023-12-09 15:50:46	\N	1	{Study,"Prof. Plum",Wrench}	\N
>>>>>>> Stashed changes
\.


--
-- Data for Name: game_states; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game_states (state_id, game_id, "timestamp", current_player, game_data) FROM stdin;
\.


--
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locations (location_name, is_restricted) FROM stdin;
Study	f
Hall	f
Hall2	t
Lounge	f
Hall3	t
Hall4	t
Hall5	t
Library	f
Hall6	t
Billiard	f
Hall7	t
Dining	f
Hall8	t
Hall9	t
Hall10	t
Conservatory	f
Hall11	t
Ballroom	f
Hall12	t
Kitchen	f
Hall1	t
ScarletStart	f
MustardStart	f
WhiteStart	f
GreenStart	f
PeacockStart	f
PlumStart	f
\.


--
-- Data for Name: player_location_map; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.player_location_map (map_id, player_id, location_name, session_id) FROM stdin;
<<<<<<< Updated upstream
=======
243	B-J529FUN0qiT1BUAAAD	Hall1	mi1tdz
>>>>>>> Stashed changes
\.


--
-- Data for Name: players; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.players (player_id, player_name, character_name, session_id) FROM stdin;
<<<<<<< Updated upstream
=======
B-J529FUN0qiT1BUAAAD	oroit	Miss Scarlet	mi1tdz
>>>>>>> Stashed changes
\.


--
-- Name: board_locations_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.board_locations_location_id_seq', 1, false);


--
-- Name: game_info_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_info_game_id_seq', 1, false);


--
-- Name: game_states_state_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_states_state_id_seq', 1, false);


--
-- Name: player_location_map_map_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.player_location_map_map_id_seq', 1025, true);


--
-- Name: player_location_map_map_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

<<<<<<< Updated upstream
SELECT pg_catalog.setval('public.player_location_map_map_id_seq1', 128, true);
=======
SELECT pg_catalog.setval('public.player_location_map_map_id_seq1', 246, true);
>>>>>>> Stashed changes


--
-- Name: players_player_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.players_player_id_seq', 1, false);


--
-- Name: locations board_locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT board_locations_pkey PRIMARY KEY (location_name);


--
-- Name: game_session game_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_session
    ADD CONSTRAINT game_info_pkey PRIMARY KEY (session_id);


--
-- Name: game_states game_states_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_states
    ADD CONSTRAINT game_states_pkey PRIMARY KEY (state_id);


--
-- Name: player_location_map player_location_map_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.player_location_map
    ADD CONSTRAINT player_location_map_pkey PRIMARY KEY (map_id);


--
-- Name: player_location_map player_location_map_player_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.player_location_map
    ADD CONSTRAINT player_location_map_player_id_key UNIQUE (player_id);


--
-- Name: players players_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (player_id);


--
-- Name: game_session game_session_player_won_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_session
    ADD CONSTRAINT game_session_player_won_fkey FOREIGN KEY (player_won) REFERENCES public.players(player_id);


--
-- Name: game_states game_states_current_player_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_states
    ADD CONSTRAINT game_states_current_player_fkey FOREIGN KEY (current_player) REFERENCES public.players(player_id);


--
-- Name: game_states game_states_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_states
    ADD CONSTRAINT game_states_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.game_session(session_id);


--
-- Name: player_location_map player_location_map_location_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.player_location_map
    ADD CONSTRAINT player_location_map_location_name_fkey FOREIGN KEY (location_name) REFERENCES public.locations(location_name);


--
-- Name: player_location_map player_location_map_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.player_location_map
    ADD CONSTRAINT player_location_map_player_id_fkey FOREIGN KEY (player_id) REFERENCES public.players(player_id);


--
-- Name: player_location_map player_location_map_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.player_location_map
    ADD CONSTRAINT player_location_map_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.game_session(session_id);


--
-- Name: players players_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.game_session(session_id);


--
-- PostgreSQL database dump complete
--

