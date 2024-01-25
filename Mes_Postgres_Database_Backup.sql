PGDMP  :                     |            dbmesdev    16.1    16.0 �    %           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            &           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            '           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            (           1262    17335    dbmesdev    DATABASE     {   CREATE DATABASE dbmesdev WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_India.1252';
    DROP DATABASE dbmesdev;
                postgres    false                       1255    17755    get_function_module_data()    FUNCTION     �  CREATE FUNCTION public.get_function_module_data() RETURNS TABLE(module_data jsonb, function_data jsonb)
    LANGUAGE plpgsql
    AS $$
DECLARE
    temp_plant_config_id INT;
BEGIN
    -- Initialize temp_plant_config_id
    SELECT json_agg(jsonb_build_object(
         'module_id', module_id,
        'module_name', module_name,
        'description', description,
        'recordstatus', recordstatus
    )) INTO module_data
    FROM Gbl_Module_Master
    WHERE recordstatus = true;
    -- Assign the result of the query to the variable for Plant_Config_Workshop
    SELECT json_agg(jsonb_build_object(
        'function_id', function_id,
        'module_id', module_id,
        'function_name', function_name,
        'description', description,
        'recordstatus', recordstatus
    )) INTO function_data
    FROM Gbl_Function_Master
    WHERE  recordstatus = true;
    -- Return the result set
    RETURN NEXT;
END 
$$;
 1   DROP FUNCTION public.get_function_module_data();
       public          postgres    false            �            1259    17380    gbl_masterdata    TABLE     �  CREATE TABLE public.gbl_masterdata (
    master_id integer NOT NULL,
    master_category character varying(50) NOT NULL,
    value character varying(50) NOT NULL,
    description character varying(100),
    recordstatus boolean DEFAULT true,
    created_by integer,
    modified_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone
);
 "   DROP TABLE public.gbl_masterdata;
       public         heap    postgres    false                       1255    17754 %   get_gbl_masterdata(character varying)    FUNCTION     	  CREATE FUNCTION public.get_gbl_masterdata(p_master_category character varying) RETURNS SETOF public.gbl_masterdata
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY 
    SELECT *
    FROM "gbl_masterdata"
    WHERE master_category = p_master_category;
END;
$$;
 N   DROP FUNCTION public.get_gbl_masterdata(p_master_category character varying);
       public          postgres    false    224            #           1255    17759    get_module_function_data() 	   PROCEDURE     p  CREATE PROCEDURE public.get_module_function_data()
    LANGUAGE plpgsql
    AS $$
DECLARE
    module_data RECORD;
    function_data RECORD;
BEGIN
    -- Select data from Gbl_Module_Master
    FOR module_data IN SELECT * FROM Gbl_Module_Master WHERE recordstatus = true
    LOOP
        -- Print or process module data as needed
        RAISE NOTICE 'Module ID: %, Module Name: %, Record Status: %',
                     module_data.module_id,
                     module_data.module_name,
                     module_data.recordstatus;
 
        -- Select associated functions for each module
        FOR function_data IN SELECT * FROM Gbl_Function_Master WHERE module_id = module_data.module_id AND recordstatus = true
        LOOP
            -- Print or process function data as needed
            RAISE NOTICE '    Function ID: %, Module ID: %, Function Name: %, Record Status: %',
                         function_data.function_id,
                         function_data.module_id,
                         function_data.function_name,
                         function_data.recordstatus;
        END LOOP;
    END LOOP;
END;
$$;
 2   DROP PROCEDURE public.get_module_function_data();
       public          postgres    false            !           1255    17752    get_plant_config_data(integer)    FUNCTION     �	  CREATE FUNCTION public.get_plant_config_data(p_plant_id integer) RETURNS TABLE(plant_config_data jsonb, plant_config_products_json jsonb, plant_config_workshops_json jsonb, plant_config_function_json jsonb)
    LANGUAGE plpgsql
    AS $$
DECLARE
    temp_plant_config_id INT;
BEGIN
    -- Initialize temp_plant_config_id
    SELECT plant_config_id INTO temp_plant_config_id 
    FROM Plant_Config 
    WHERE plant_id = p_plant_id;
    -- Fetch the data for Plant_Config as JSONB
    SELECT jsonb_build_object(
        'plant_config_id', plant_config_id,
		'plant_id', plant_id,
        'plant_name', plant_name,
        'area_code', area_code,
        'plant_address', plant_address,
        'timezone_id', timezone_id,
        'language_id', language_id,
        'unit_id', unit_id,
        'currency_id', currency_id,
        'shift1_from', shift1_from,
        'shift1_to', shift1_to,
        'shift2_from', shift2_from,
        'shift2_to', shift2_to,
        'shift3_from', shift3_from,
        'shift3_to', shift3_to,
        'created_at', created_at,
        'modified_at', modified_at,
        'modified_by', modified_by,
        'created_by', created_by,
        'record_status', record_status
    ) INTO plant_config_data
    FROM Plant_Config
    WHERE plant_config_id = temp_plant_config_id;
    -- Assign the result of the query to the variable for Plant_Config_Product
    SELECT json_agg(jsonb_build_object(
        'plant_product_id', plant_product_id,
        'plant_config_id', plant_config_id,
        'product_id', product_id,
        'product_name', product_name,
        'record_status', record_status
    )) INTO plant_config_products_Json
    FROM Plant_Config_Product
    WHERE plant_config_id = temp_plant_config_id AND record_status = true;
    -- Assign the result of the query to the variable for Plant_Config_Workshop
    SELECT json_agg(jsonb_build_object(
        'plant_workshop_id', plant_workshop_id,
        'plant_config_id', plant_config_id,
        'workshop_id', workshop_id,
        'workshop_name', workshop_name,
        'record_status', record_status
    )) INTO plant_config_workshops_Json
    FROM Plant_Config_Workshop
    WHERE plant_config_id = temp_plant_config_id AND record_status = true;
 
	SELECT json_agg(jsonb_build_object(
        'module_id', module_id,
        'function_id', function_id
    )) INTO plant_config_function_Json
    FROM Plant_function_Master
    WHERE plant_id = p_plant_id AND record_status = true;
    -- Return the result set
    RETURN NEXT;
END 
$$;
 @   DROP FUNCTION public.get_plant_config_data(p_plant_id integer);
       public          postgres    false            $           1255    17782 U  insert_plant_configuration(integer, character varying, character varying, character varying, integer, integer, integer, integer, timestamp without time zone, timestamp without time zone, timestamp without time zone, timestamp without time zone, timestamp without time zone, timestamp without time zone, integer, integer, jsonb, jsonb, jsonb) 	   PROCEDURE     �  CREATE PROCEDURE public.insert_plant_configuration(IN p_plant_id integer, IN p_plant_name character varying, IN p_area_code character varying, IN p_plant_address character varying, IN p_timezone_id integer, IN p_language_id integer, IN p_unit_id integer, IN p_currency_id integer, IN p_shift1_from timestamp without time zone, IN p_shift1_to timestamp without time zone, IN p_shift2_from timestamp without time zone, IN p_shift2_to timestamp without time zone, IN p_shift3_from timestamp without time zone, IN p_shift3_to timestamp without time zone, IN p_created_by integer, IN p_modified_by integer, IN p_products_json jsonb, IN p_workshops_json jsonb, IN p_function_json jsonb)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_plant_config_id INT;
    product_data jsonb;
    workshop_data jsonb;
	function_data jsonb;
BEGIN
    -- Insert into Plant_Config table
    INSERT INTO Plant_Config (
        plant_id,
        plant_name,
        area_code,
        plant_address,
        timezone_id,
        language_id,
        unit_id,
        currency_id,
        shift1_from,
        shift1_to,
        shift2_from,
        shift2_to,
        shift3_from,
        shift3_to,
        created_at,
        modified_at,
        modified_by,
        created_by
    ) VALUES (
        p_plant_id,
        p_plant_name,
        p_area_code,
        p_plant_address,
        p_timezone_id,
        p_language_id,
        p_unit_id,
        p_currency_id,
        p_shift1_from,
        p_shift1_to,
        p_shift2_from,
        p_shift2_to,
        p_shift3_from,
        p_shift3_to,
        current_timestamp,
        current_timestamp,
        p_modified_by,
        p_created_by
    )
    RETURNING plant_config_id INTO v_plant_config_id;
    -- Insert into Plant_Config_Product table
    FOR product_data IN SELECT * FROM jsonb_array_elements(p_products_json)
    LOOP
        INSERT INTO Plant_Config_Product (
            plant_config_id,
            product_id,
            created_by,
            modified_by,
            created_at,
            modified_at
        ) VALUES (
            v_plant_config_id,
            (product_data->>'product_id')::INT,
            p_created_by,
            DEFAULT,  -- Use DEFAULT for modified_by
            current_timestamp,
            DEFAULT  -- Use DEFAULT for modified_at
        );
    END LOOP;
    -- Insert into Plant_Config_Workshop table
    FOR workshop_data IN SELECT * FROM jsonb_array_elements(p_workshops_json)
    LOOP
        INSERT INTO Plant_Config_Workshop (
            plant_workshop_id,
            plant_config_id,
            workshop_id,
            workshop_name,
            created_by,
            modified_by,
            created_at,
            modified_at
        ) VALUES (
            DEFAULT,  -- Assuming plant_workshop_id is a serial type
            v_plant_config_id,
            (workshop_data->>'workshop_id')::INT,
            (workshop_data->>'workshop_name')::VARCHAR(500),
            p_created_by,
            DEFAULT,  -- Use DEFAULT for modified_by
            current_timestamp,
            DEFAULT  -- Use DEFAULT for modified_at
        );
    END LOOP;
	 -- Insert into Plant_function_Master table
    FOR function_data IN SELECT * FROM jsonb_array_elements(p_function_json)
    LOOP
        INSERT INTO Plant_function_Master (
            plant_function_id,
            plant_id,
            module_id,
            function_id,
            created_by,
            created_at
        ) VALUES (
            DEFAULT,  -- Assuming plant_workshop_id is a serial type
            p_plant_id,
            (function_data->>'module_id')::INT,
            (function_data->>'function_id')::INT,
            p_created_by,
            current_timestamp
        );
    END LOOP;
END;
$$;
 �  DROP PROCEDURE public.insert_plant_configuration(IN p_plant_id integer, IN p_plant_name character varying, IN p_area_code character varying, IN p_plant_address character varying, IN p_timezone_id integer, IN p_language_id integer, IN p_unit_id integer, IN p_currency_id integer, IN p_shift1_from timestamp without time zone, IN p_shift1_to timestamp without time zone, IN p_shift2_from timestamp without time zone, IN p_shift2_to timestamp without time zone, IN p_shift3_from timestamp without time zone, IN p_shift3_to timestamp without time zone, IN p_created_by integer, IN p_modified_by integer, IN p_products_json jsonb, IN p_workshops_json jsonb, IN p_function_json jsonb);
       public          postgres    false            "           1255    17758 (   select_gbl_masterdata(character varying) 	   PROCEDURE     �  CREATE PROCEDURE public.select_gbl_masterdata(IN p_master_category character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
    SELECT
        Gbl_MasterData.master_id,
        Gbl_MasterData.master_category,
        Gbl_MasterData.value,
        Gbl_MasterData.description,
        Gbl_MasterData.recordstatus
 
    FROM
        Gbl_MasterData
    WHERE
        Gbl_MasterData.master_category = p_master_category
        AND Gbl_MasterData.recordstatus = true;
END;
$$;
 U   DROP PROCEDURE public.select_gbl_masterdata(IN p_master_category character varying);
       public          postgres    false            %           1255    17757   update_plant_configuration(integer, character varying, integer, timestamp without time zone, timestamp without time zone, timestamp without time zone, timestamp without time zone, timestamp without time zone, timestamp without time zone, integer, jsonb, jsonb, jsonb) 	   PROCEDURE     w  CREATE PROCEDURE public.update_plant_configuration(IN p_plant_id integer, IN p_plant_address character varying, IN p_language_id integer, IN p_shift1_from timestamp without time zone, IN p_shift1_to timestamp without time zone, IN p_shift2_from timestamp without time zone, IN p_shift2_to timestamp without time zone, IN p_shift3_from timestamp without time zone, IN p_shift3_to timestamp without time zone, IN p_modified_by integer, IN p_products_json jsonb, IN p_workshops_json jsonb, IN p_function_json jsonb)
    LANGUAGE plpgsql
    AS $$
DECLARE
    product_data jsonb;
    workshop_data jsonb;
    function_data jsonb;
    temp_plant_config_id INT;
BEGIN
    SELECT plant_config_id INTO temp_plant_config_id 
    FROM Plant_Config 
    WHERE plant_id = p_plant_id;

    -- Update Plant_Config table
    UPDATE Plant_Config
    SET
        plant_address = p_plant_address,
        language_id = p_language_id,
        shift1_from = p_shift1_from,
        shift1_to = p_shift1_to,
        shift2_from = p_shift2_from,
        shift2_to = p_shift2_to,
        shift3_from = p_shift3_from,
        shift3_to = p_shift3_to,
        modified_at = current_timestamp,
        modified_by = p_modified_by
    WHERE plant_id = p_plant_id;

    DELETE FROM Plant_Config_Product WHERE plant_config_id = temp_plant_config_id;

    -- Insert or update Plant_Config_Product records
    FOR product_data IN SELECT * FROM jsonb_array_elements(p_products_json)
    LOOP
        INSERT INTO Plant_Config_Product (
            plant_config_id,
            product_id,
            created_by,
            modified_by,
            created_at,
            modified_at
        ) VALUES (
            temp_plant_config_id,
            (product_data->>'product_id')::INT,
            p_modified_by,
            NULL,  -- Modify if there is a modified_by value
            current_timestamp,
            NULL  -- Modify if there is a modified_at value
        )
        ON CONFLICT (plant_config_id, product_id) DO UPDATE
        SET
            modified_by = p_modified_by,
            modified_at = current_timestamp;
    END LOOP;

    -- Insert or update Plant_Config_Workshop records
    FOR workshop_data IN SELECT * FROM jsonb_array_elements(p_workshops_json)
    LOOP
        INSERT INTO Plant_Config_Workshop (
            plant_workshop_id,
            plant_config_id,
            workshop_id,
            workshop_name,
            created_by,
            modified_by,
            created_at,
            modified_at
        ) VALUES (
            DEFAULT,  -- Assuming plant_workshop_id is a serial type
            temp_plant_config_id,
            (workshop_data->>'workshop_id')::INT,
            (workshop_data->>'workshop_name')::VARCHAR(500),
            p_modified_by,
            NULL,  -- Modify if there is a modified_by value
            current_timestamp,
            NULL  -- Modify if there is a modified_at value
        )
        ON CONFLICT (plant_config_id, workshop_id) DO UPDATE
        SET
            workshop_id = (workshop_data->>'workshop_id')::INT,
            workshop_name = (workshop_data->>'workshop_name')::VARCHAR(500),
			record_status = (workshop_data->>'record_status')::BOOLEAN,
            modified_by = p_modified_by,
            modified_at = current_timestamp;
    END LOOP;

    -- Delete records from Plant_function_Master
    DELETE FROM Plant_function_Master WHERE plant_id = p_plant_id;

    -- Insert or update Plant_function_Master records
    FOR function_data IN SELECT * FROM jsonb_array_elements(p_function_json)
    LOOP
        INSERT INTO Plant_function_Master (
            plant_function_id,
            plant_id,
            module_id,
            function_id,
            modified_by,
            modified_at
        ) VALUES (
            DEFAULT,  -- Assuming plant_function_id is a serial type
            p_plant_id,
            (function_data->>'module_id')::INT,
            COALESCE((function_data->>'function_id')::INT, 0),  -- Handle if function_id is not present in JSON
            p_modified_by,
            current_timestamp
        )
        ON CONFLICT (plant_id, module_id, function_id) DO UPDATE
        SET
            module_id = (function_data->>'module_id')::INT,
            function_id = COALESCE((function_data->>'function_id')::INT, 0),  -- Handle if function_id is not present in JSON
            modified_by = p_modified_by,
            modified_at = current_timestamp;
    END LOOP;
END;
$$;
    DROP PROCEDURE public.update_plant_configuration(IN p_plant_id integer, IN p_plant_address character varying, IN p_language_id integer, IN p_shift1_from timestamp without time zone, IN p_shift1_to timestamp without time zone, IN p_shift2_from timestamp without time zone, IN p_shift2_to timestamp without time zone, IN p_shift3_from timestamp without time zone, IN p_shift3_to timestamp without time zone, IN p_modified_by integer, IN p_products_json jsonb, IN p_workshops_json jsonb, IN p_function_json jsonb);
       public          postgres    false            �            1259    17654    app_currency    TABLE     g   CREATE TABLE public.app_currency (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);
     DROP TABLE public.app_currency;
       public         heap    postgres    false            �            1259    17653    app_currency_id_seq    SEQUENCE     �   ALTER TABLE public.app_currency ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_currency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    254                        1259    17660    app_erp    TABLE     b   CREATE TABLE public.app_erp (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);
    DROP TABLE public.app_erp;
       public         heap    postgres    false            �            1259    17659    app_erp_id_seq    SEQUENCE     �   ALTER TABLE public.app_erp ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_erp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    256                       1259    17666    app_function    TABLE     g   CREATE TABLE public.app_function (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);
     DROP TABLE public.app_function;
       public         heap    postgres    false                       1259    17665    app_function_id_seq    SEQUENCE     �   ALTER TABLE public.app_function ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_function_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    258                       1259    17672    app_language    TABLE     g   CREATE TABLE public.app_language (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);
     DROP TABLE public.app_language;
       public         heap    postgres    false                       1259    17671    app_language_id_seq    SEQUENCE     �   ALTER TABLE public.app_language ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_language_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    260                       1259    17678    app_plantconfig    TABLE     j   CREATE TABLE public.app_plantconfig (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);
 #   DROP TABLE public.app_plantconfig;
       public         heap    postgres    false                       1259    17677    app_plantconfig_id_seq    SEQUENCE     �   ALTER TABLE public.app_plantconfig ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_plantconfig_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    262                       1259    17684    app_product    TABLE     f   CREATE TABLE public.app_product (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);
    DROP TABLE public.app_product;
       public         heap    postgres    false                       1259    17683    app_product_id_seq    SEQUENCE     �   ALTER TABLE public.app_product ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    264            
           1259    17690    app_timezone    TABLE     g   CREATE TABLE public.app_timezone (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);
     DROP TABLE public.app_timezone;
       public         heap    postgres    false            	           1259    17689    app_timezone_id_seq    SEQUENCE     �   ALTER TABLE public.app_timezone ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_timezone_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    266                       1259    17696    app_unit    TABLE     c   CREATE TABLE public.app_unit (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);
    DROP TABLE public.app_unit;
       public         heap    postgres    false                       1259    17695    app_unit_id_seq    SEQUENCE     �   ALTER TABLE public.app_unit ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_unit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    268            �            1259    17541 
   auth_group    TABLE     f   CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
    DROP TABLE public.auth_group;
       public         heap    postgres    false            �            1259    17540    auth_group_id_seq    SEQUENCE     �   ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    242            �            1259    17549    auth_group_permissions    TABLE     �   CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public         heap    postgres    false            �            1259    17548    auth_group_permissions_id_seq    SEQUENCE     �   ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    244            �            1259    17535    auth_permission    TABLE     �   CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public         heap    postgres    false            �            1259    17534    auth_permission_id_seq    SEQUENCE     �   ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    240            �            1259    17555 	   auth_user    TABLE     �  CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
    DROP TABLE public.auth_user;
       public         heap    postgres    false            �            1259    17563    auth_user_groups    TABLE     ~   CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
 $   DROP TABLE public.auth_user_groups;
       public         heap    postgres    false            �            1259    17562    auth_user_groups_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    248            �            1259    17554    auth_user_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    246            �            1259    17569    auth_user_user_permissions    TABLE     �   CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
 .   DROP TABLE public.auth_user_user_permissions;
       public         heap    postgres    false            �            1259    17568 !   auth_user_user_permissions_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    250            �            1259    17627    django_admin_log    TABLE     �  CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
 $   DROP TABLE public.django_admin_log;
       public         heap    postgres    false            �            1259    17626    django_admin_log_id_seq    SEQUENCE     �   ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    252            �            1259    17527    django_content_type    TABLE     �   CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public         heap    postgres    false            �            1259    17526    django_content_type_id_seq    SEQUENCE     �   ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    238            �            1259    17519    django_migrations    TABLE     �   CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
 %   DROP TABLE public.django_migrations;
       public         heap    postgres    false            �            1259    17518    django_migrations_id_seq    SEQUENCE     �   ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    236                       1259    17709    django_session    TABLE     �   CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
 "   DROP TABLE public.django_session;
       public         heap    postgres    false            �            1259    17346    gbl_function_master    TABLE     �  CREATE TABLE public.gbl_function_master (
    function_id integer NOT NULL,
    module_id integer NOT NULL,
    function_name character varying(50) NOT NULL,
    description character varying(100),
    created_by integer,
    modified_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone,
    recordstatus boolean DEFAULT true
);
 '   DROP TABLE public.gbl_function_master;
       public         heap    postgres    false            �            1259    17345 #   gbl_function_master_function_id_seq    SEQUENCE     �   CREATE SEQUENCE public.gbl_function_master_function_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 :   DROP SEQUENCE public.gbl_function_master_function_id_seq;
       public          postgres    false    218            )           0    0 #   gbl_function_master_function_id_seq    SEQUENCE OWNED BY     k   ALTER SEQUENCE public.gbl_function_master_function_id_seq OWNED BY public.gbl_function_master.function_id;
          public          postgres    false    217            �            1259    17379    gbl_masterdata_master_id_seq    SEQUENCE     �   CREATE SEQUENCE public.gbl_masterdata_master_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.gbl_masterdata_master_id_seq;
       public          postgres    false    224            *           0    0    gbl_masterdata_master_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.gbl_masterdata_master_id_seq OWNED BY public.gbl_masterdata.master_id;
          public          postgres    false    223            �            1259    17337    gbl_module_master    TABLE     v  CREATE TABLE public.gbl_module_master (
    module_id integer NOT NULL,
    module_name character varying(50) NOT NULL,
    description character varying(100),
    recordstatus boolean DEFAULT true,
    created_by integer,
    modified_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone
);
 %   DROP TABLE public.gbl_module_master;
       public         heap    postgres    false            �            1259    17336    gbl_module_master_module_id_seq    SEQUENCE     �   CREATE SEQUENCE public.gbl_module_master_module_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.gbl_module_master_module_id_seq;
       public          postgres    false    216            +           0    0    gbl_module_master_module_id_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.gbl_module_master_module_id_seq OWNED BY public.gbl_module_master.module_id;
          public          postgres    false    215            �            1259    17360 	   gbl_users    TABLE     �  CREATE TABLE public.gbl_users (
    user_id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    phone character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    department character varying(50) NOT NULL,
    login_type character varying(50) NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(100) NOT NULL,
    is_active boolean DEFAULT true,
    record_status boolean DEFAULT true,
    created_by integer NOT NULL,
    modified_by integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone NOT NULL,
    row_guid uuid NOT NULL
);
    DROP TABLE public.gbl_users;
       public         heap    postgres    false            �            1259    17359    gbl_users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.gbl_users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.gbl_users_user_id_seq;
       public          postgres    false    220            ,           0    0    gbl_users_user_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.gbl_users_user_id_seq OWNED BY public.gbl_users.user_id;
          public          postgres    false    219            �            1259    17398    plant_config    TABLE     �  CREATE TABLE public.plant_config (
    plant_config_id integer NOT NULL,
    plant_id integer NOT NULL,
    plant_name character varying(50) NOT NULL,
    area_code character varying(50) NOT NULL,
    plant_address character varying(50) NOT NULL,
    timezone_id integer NOT NULL,
    language_id integer NOT NULL,
    unit_id integer NOT NULL,
    currency_id integer NOT NULL,
    shift1_from timestamp without time zone NOT NULL,
    shift1_to timestamp without time zone NOT NULL,
    shift2_from timestamp without time zone NOT NULL,
    shift2_to timestamp without time zone NOT NULL,
    shift3_from timestamp without time zone NOT NULL,
    shift3_to timestamp without time zone NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone,
    modified_by integer NOT NULL,
    created_by integer NOT NULL,
    record_status boolean DEFAULT true,
    row_guid uuid
);
     DROP TABLE public.plant_config;
       public         heap    postgres    false            �            1259    17397     plant_config_plant_config_id_seq    SEQUENCE     �   CREATE SEQUENCE public.plant_config_plant_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.plant_config_plant_config_id_seq;
       public          postgres    false    228            -           0    0     plant_config_plant_config_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.plant_config_plant_config_id_seq OWNED BY public.plant_config.plant_config_id;
          public          postgres    false    227                       1259    17736    plant_config_product    TABLE     �  CREATE TABLE public.plant_config_product (
    plant_product_id integer NOT NULL,
    plant_config_id integer NOT NULL,
    product_id integer NOT NULL,
    product_name character varying(200),
    created_by integer,
    modified_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone,
    record_status boolean DEFAULT true
);
 (   DROP TABLE public.plant_config_product;
       public         heap    postgres    false                       1259    17735 )   plant_config_product_plant_product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.plant_config_product_plant_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 @   DROP SEQUENCE public.plant_config_product_plant_product_id_seq;
       public          postgres    false    273            .           0    0 )   plant_config_product_plant_product_id_seq    SEQUENCE OWNED BY     w   ALTER SEQUENCE public.plant_config_product_plant_product_id_seq OWNED BY public.plant_config_product.plant_product_id;
          public          postgres    false    272                       1259    17720    plant_config_workshop    TABLE     �  CREATE TABLE public.plant_config_workshop (
    plant_workshop_id integer NOT NULL,
    plant_config_id integer NOT NULL,
    workshop_id integer NOT NULL,
    workshop_name character varying(500) NOT NULL,
    created_by integer,
    modified_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone,
    record_status boolean DEFAULT true
);
 )   DROP TABLE public.plant_config_workshop;
       public         heap    postgres    false                       1259    17719 +   plant_config_workshop_plant_workshop_id_seq    SEQUENCE     �   CREATE SEQUENCE public.plant_config_workshop_plant_workshop_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 B   DROP SEQUENCE public.plant_config_workshop_plant_workshop_id_seq;
       public          postgres    false    271            /           0    0 +   plant_config_workshop_plant_workshop_id_seq    SEQUENCE OWNED BY     {   ALTER SEQUENCE public.plant_config_workshop_plant_workshop_id_seq OWNED BY public.plant_config_workshop.plant_workshop_id;
          public          postgres    false    270                       1259    17803    plant_function_master    TABLE     �  CREATE TABLE public.plant_function_master (
    plant_function_id integer NOT NULL,
    plant_id integer NOT NULL,
    module_id integer NOT NULL,
    function_id integer NOT NULL,
    created_by integer,
    modified_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone,
    record_status boolean DEFAULT true
);
 )   DROP TABLE public.plant_function_master;
       public         heap    postgres    false                       1259    17802 +   plant_function_master_plant_function_id_seq    SEQUENCE     �   CREATE SEQUENCE public.plant_function_master_plant_function_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 B   DROP SEQUENCE public.plant_function_master_plant_function_id_seq;
       public          postgres    false    275            0           0    0 +   plant_function_master_plant_function_id_seq    SEQUENCE OWNED BY     {   ALTER SEQUENCE public.plant_function_master_plant_function_id_seq OWNED BY public.plant_function_master.plant_function_id;
          public          postgres    false    274            �            1259    17389    plant_master    TABLE     m  CREATE TABLE public.plant_master (
    plant_id integer NOT NULL,
    plant_name character varying(50) NOT NULL,
    recordstatus boolean DEFAULT true,
    created_by integer,
    modified_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone,
    area_code character varying(200)
);
     DROP TABLE public.plant_master;
       public         heap    postgres    false            �            1259    17388    plant_master_plant_id_seq    SEQUENCE     �   CREATE SEQUENCE public.plant_master_plant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.plant_master_plant_id_seq;
       public          postgres    false    226            1           0    0    plant_master_plant_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.plant_master_plant_id_seq OWNED BY public.plant_master.plant_id;
          public          postgres    false    225            �            1259    17370 
   plant_role    TABLE     �  CREATE TABLE public.plant_role (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL,
    created_by integer NOT NULL,
    modified_by integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone NOT NULL,
    is_active boolean DEFAULT true,
    record_status boolean DEFAULT true,
    row_guid uuid NOT NULL
);
    DROP TABLE public.plant_role;
       public         heap    postgres    false            �            1259    17369    plant_role_role_id_seq    SEQUENCE     �   CREATE SEQUENCE public.plant_role_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.plant_role_role_id_seq;
       public          postgres    false    222            2           0    0    plant_role_role_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.plant_role_role_id_seq OWNED BY public.plant_role.role_id;
          public          postgres    false    221            �            1259    17431    plant_user_role    TABLE     a  CREATE TABLE public.plant_user_role (
    user_role_id integer NOT NULL,
    plant_user_id integer NOT NULL,
    role_id integer NOT NULL,
    recordstatus boolean DEFAULT true,
    created_by integer,
    modified_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone
);
 #   DROP TABLE public.plant_user_role;
       public         heap    postgres    false            �            1259    17430     plant_user_role_user_role_id_seq    SEQUENCE     �   CREATE SEQUENCE public.plant_user_role_user_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.plant_user_role_user_role_id_seq;
       public          postgres    false    232            3           0    0     plant_user_role_user_role_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.plant_user_role_user_role_id_seq OWNED BY public.plant_user_role.user_role_id;
          public          postgres    false    231            �            1259    17412    plant_users    TABLE     Y  CREATE TABLE public.plant_users (
    plant_user_id integer NOT NULL,
    plant_id integer NOT NULL,
    user_id integer NOT NULL,
    recordstatus boolean DEFAULT true,
    created_by integer,
    modified_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone
);
    DROP TABLE public.plant_users;
       public         heap    postgres    false            �            1259    17411    plant_users_plant_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.plant_users_plant_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.plant_users_plant_user_id_seq;
       public          postgres    false    230            4           0    0    plant_users_plant_user_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.plant_users_plant_user_id_seq OWNED BY public.plant_users.plant_user_id;
          public          postgres    false    229            �            1259    17450    role_permission    TABLE       CREATE TABLE public.role_permission (
    role_permission_id integer NOT NULL,
    role_id integer NOT NULL,
    function_id integer NOT NULL,
    "create" boolean DEFAULT false,
    edit boolean DEFAULT false,
    delete boolean DEFAULT false,
    read boolean DEFAULT false,
    plant_id integer NOT NULL,
    created_by integer,
    modified_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at timestamp without time zone,
    record_status boolean DEFAULT true
);
 #   DROP TABLE public.role_permission;
       public         heap    postgres    false            �            1259    17449 &   role_permission_role_permission_id_seq    SEQUENCE     �   CREATE SEQUENCE public.role_permission_role_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 =   DROP SEQUENCE public.role_permission_role_permission_id_seq;
       public          postgres    false    234            5           0    0 &   role_permission_role_permission_id_seq    SEQUENCE OWNED BY     q   ALTER SEQUENCE public.role_permission_role_permission_id_seq OWNED BY public.role_permission.role_permission_id;
          public          postgres    false    233            �           2604    17349    gbl_function_master function_id    DEFAULT     �   ALTER TABLE ONLY public.gbl_function_master ALTER COLUMN function_id SET DEFAULT nextval('public.gbl_function_master_function_id_seq'::regclass);
 N   ALTER TABLE public.gbl_function_master ALTER COLUMN function_id DROP DEFAULT;
       public          postgres    false    218    217    218            �           2604    17383    gbl_masterdata master_id    DEFAULT     �   ALTER TABLE ONLY public.gbl_masterdata ALTER COLUMN master_id SET DEFAULT nextval('public.gbl_masterdata_master_id_seq'::regclass);
 G   ALTER TABLE public.gbl_masterdata ALTER COLUMN master_id DROP DEFAULT;
       public          postgres    false    223    224    224            �           2604    17340    gbl_module_master module_id    DEFAULT     �   ALTER TABLE ONLY public.gbl_module_master ALTER COLUMN module_id SET DEFAULT nextval('public.gbl_module_master_module_id_seq'::regclass);
 J   ALTER TABLE public.gbl_module_master ALTER COLUMN module_id DROP DEFAULT;
       public          postgres    false    216    215    216            �           2604    17363    gbl_users user_id    DEFAULT     v   ALTER TABLE ONLY public.gbl_users ALTER COLUMN user_id SET DEFAULT nextval('public.gbl_users_user_id_seq'::regclass);
 @   ALTER TABLE public.gbl_users ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    219    220    220            �           2604    17401    plant_config plant_config_id    DEFAULT     �   ALTER TABLE ONLY public.plant_config ALTER COLUMN plant_config_id SET DEFAULT nextval('public.plant_config_plant_config_id_seq'::regclass);
 K   ALTER TABLE public.plant_config ALTER COLUMN plant_config_id DROP DEFAULT;
       public          postgres    false    227    228    228            �           2604    17739 %   plant_config_product plant_product_id    DEFAULT     �   ALTER TABLE ONLY public.plant_config_product ALTER COLUMN plant_product_id SET DEFAULT nextval('public.plant_config_product_plant_product_id_seq'::regclass);
 T   ALTER TABLE public.plant_config_product ALTER COLUMN plant_product_id DROP DEFAULT;
       public          postgres    false    272    273    273            �           2604    17723 '   plant_config_workshop plant_workshop_id    DEFAULT     �   ALTER TABLE ONLY public.plant_config_workshop ALTER COLUMN plant_workshop_id SET DEFAULT nextval('public.plant_config_workshop_plant_workshop_id_seq'::regclass);
 V   ALTER TABLE public.plant_config_workshop ALTER COLUMN plant_workshop_id DROP DEFAULT;
       public          postgres    false    271    270    271            �           2604    17806 '   plant_function_master plant_function_id    DEFAULT     �   ALTER TABLE ONLY public.plant_function_master ALTER COLUMN plant_function_id SET DEFAULT nextval('public.plant_function_master_plant_function_id_seq'::regclass);
 V   ALTER TABLE public.plant_function_master ALTER COLUMN plant_function_id DROP DEFAULT;
       public          postgres    false    275    274    275            �           2604    17392    plant_master plant_id    DEFAULT     ~   ALTER TABLE ONLY public.plant_master ALTER COLUMN plant_id SET DEFAULT nextval('public.plant_master_plant_id_seq'::regclass);
 D   ALTER TABLE public.plant_master ALTER COLUMN plant_id DROP DEFAULT;
       public          postgres    false    226    225    226            �           2604    17373    plant_role role_id    DEFAULT     x   ALTER TABLE ONLY public.plant_role ALTER COLUMN role_id SET DEFAULT nextval('public.plant_role_role_id_seq'::regclass);
 A   ALTER TABLE public.plant_role ALTER COLUMN role_id DROP DEFAULT;
       public          postgres    false    222    221    222            �           2604    17434    plant_user_role user_role_id    DEFAULT     �   ALTER TABLE ONLY public.plant_user_role ALTER COLUMN user_role_id SET DEFAULT nextval('public.plant_user_role_user_role_id_seq'::regclass);
 K   ALTER TABLE public.plant_user_role ALTER COLUMN user_role_id DROP DEFAULT;
       public          postgres    false    231    232    232            �           2604    17415    plant_users plant_user_id    DEFAULT     �   ALTER TABLE ONLY public.plant_users ALTER COLUMN plant_user_id SET DEFAULT nextval('public.plant_users_plant_user_id_seq'::regclass);
 H   ALTER TABLE public.plant_users ALTER COLUMN plant_user_id DROP DEFAULT;
       public          postgres    false    229    230    230            �           2604    17453 "   role_permission role_permission_id    DEFAULT     �   ALTER TABLE ONLY public.role_permission ALTER COLUMN role_permission_id SET DEFAULT nextval('public.role_permission_role_permission_id_seq'::regclass);
 Q   ALTER TABLE public.role_permission ALTER COLUMN role_permission_id DROP DEFAULT;
       public          postgres    false    233    234    234                      0    17654    app_currency 
   TABLE DATA           0   COPY public.app_currency (id, name) FROM stdin;
    public          postgres    false    254   xw                0    17660    app_erp 
   TABLE DATA           +   COPY public.app_erp (id, name) FROM stdin;
    public          postgres    false    256   �w                0    17666    app_function 
   TABLE DATA           0   COPY public.app_function (id, name) FROM stdin;
    public          postgres    false    258   �w                0    17672    app_language 
   TABLE DATA           0   COPY public.app_language (id, name) FROM stdin;
    public          postgres    false    260   �w                0    17678    app_plantconfig 
   TABLE DATA           3   COPY public.app_plantconfig (id, name) FROM stdin;
    public          postgres    false    262   �w                0    17684    app_product 
   TABLE DATA           /   COPY public.app_product (id, name) FROM stdin;
    public          postgres    false    264   	x                0    17690    app_timezone 
   TABLE DATA           0   COPY public.app_timezone (id, name) FROM stdin;
    public          postgres    false    266   &x                0    17696    app_unit 
   TABLE DATA           ,   COPY public.app_unit (id, name) FROM stdin;
    public          postgres    false    268   Cx                0    17541 
   auth_group 
   TABLE DATA           .   COPY public.auth_group (id, name) FROM stdin;
    public          postgres    false    242   `x                0    17549    auth_group_permissions 
   TABLE DATA           M   COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
    public          postgres    false    244   }x      �          0    17535    auth_permission 
   TABLE DATA           N   COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
    public          postgres    false    240   �x                0    17555 	   auth_user 
   TABLE DATA           �   COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
    public          postgres    false    246   �z                0    17563    auth_user_groups 
   TABLE DATA           A   COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
    public          postgres    false    248   �z      	          0    17569    auth_user_user_permissions 
   TABLE DATA           P   COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
    public          postgres    false    250   	{                0    17627    django_admin_log 
   TABLE DATA           �   COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
    public          postgres    false    252   &{      �          0    17527    django_content_type 
   TABLE DATA           C   COPY public.django_content_type (id, app_label, model) FROM stdin;
    public          postgres    false    238   C{      �          0    17519    django_migrations 
   TABLE DATA           C   COPY public.django_migrations (id, app, name, applied) FROM stdin;
    public          postgres    false    236   �{                0    17709    django_session 
   TABLE DATA           P   COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
    public          postgres    false    269   �}      �          0    17346    gbl_function_master 
   TABLE DATA           �   COPY public.gbl_function_master (function_id, module_id, function_name, description, created_by, modified_by, created_at, modified_at, recordstatus) FROM stdin;
    public          postgres    false    218   �}      �          0    17380    gbl_masterdata 
   TABLE DATA           �   COPY public.gbl_masterdata (master_id, master_category, value, description, recordstatus, created_by, modified_by, created_at, modified_at) FROM stdin;
    public          postgres    false    224   ]      �          0    17337    gbl_module_master 
   TABLE DATA           �   COPY public.gbl_module_master (module_id, module_name, description, recordstatus, created_by, modified_by, created_at, modified_at) FROM stdin;
    public          postgres    false    216   w�      �          0    17360 	   gbl_users 
   TABLE DATA           �   COPY public.gbl_users (user_id, first_name, last_name, phone, email, department, login_type, username, password, is_active, record_status, created_by, modified_by, created_at, modified_at, row_guid) FROM stdin;
    public          postgres    false    220   �      �          0    17398    plant_config 
   TABLE DATA           *  COPY public.plant_config (plant_config_id, plant_id, plant_name, area_code, plant_address, timezone_id, language_id, unit_id, currency_id, shift1_from, shift1_to, shift2_from, shift2_to, shift3_from, shift3_to, created_at, modified_at, modified_by, created_by, record_status, row_guid) FROM stdin;
    public          postgres    false    228   �                 0    17736    plant_config_product 
   TABLE DATA           �   COPY public.plant_config_product (plant_product_id, plant_config_id, product_id, product_name, created_by, modified_by, created_at, modified_at, record_status) FROM stdin;
    public          postgres    false    273   <�                0    17720    plant_config_workshop 
   TABLE DATA           �   COPY public.plant_config_workshop (plant_workshop_id, plant_config_id, workshop_id, workshop_name, created_by, modified_by, created_at, modified_at, record_status) FROM stdin;
    public          postgres    false    271   Y�      "          0    17803    plant_function_master 
   TABLE DATA           �   COPY public.plant_function_master (plant_function_id, plant_id, module_id, function_id, created_by, modified_by, created_at, modified_at, record_status) FROM stdin;
    public          postgres    false    275   v�      �          0    17389    plant_master 
   TABLE DATA           �   COPY public.plant_master (plant_id, plant_name, recordstatus, created_by, modified_by, created_at, modified_at, area_code) FROM stdin;
    public          postgres    false    226   ��      �          0    17370 
   plant_role 
   TABLE DATA           �   COPY public.plant_role (role_id, role_name, created_by, modified_by, created_at, modified_at, is_active, record_status, row_guid) FROM stdin;
    public          postgres    false    222   �      �          0    17431    plant_user_role 
   TABLE DATA           �   COPY public.plant_user_role (user_role_id, plant_user_id, role_id, recordstatus, created_by, modified_by, created_at, modified_at) FROM stdin;
    public          postgres    false    232   �      �          0    17412    plant_users 
   TABLE DATA           �   COPY public.plant_users (plant_user_id, plant_id, user_id, recordstatus, created_by, modified_by, created_at, modified_at) FROM stdin;
    public          postgres    false    230   �      �          0    17450    role_permission 
   TABLE DATA           �   COPY public.role_permission (role_permission_id, role_id, function_id, "create", edit, delete, read, plant_id, created_by, modified_by, created_at, modified_at, record_status) FROM stdin;
    public          postgres    false    234   ;�      6           0    0    app_currency_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.app_currency_id_seq', 1, false);
          public          postgres    false    253            7           0    0    app_erp_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.app_erp_id_seq', 1, false);
          public          postgres    false    255            8           0    0    app_function_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.app_function_id_seq', 1, false);
          public          postgres    false    257            9           0    0    app_language_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.app_language_id_seq', 1, false);
          public          postgres    false    259            :           0    0    app_plantconfig_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.app_plantconfig_id_seq', 1, false);
          public          postgres    false    261            ;           0    0    app_product_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.app_product_id_seq', 1, false);
          public          postgres    false    263            <           0    0    app_timezone_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.app_timezone_id_seq', 1, false);
          public          postgres    false    265            =           0    0    app_unit_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.app_unit_id_seq', 1, false);
          public          postgres    false    267            >           0    0    auth_group_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);
          public          postgres    false    241            ?           0    0    auth_group_permissions_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);
          public          postgres    false    243            @           0    0    auth_permission_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.auth_permission_id_seq', 56, true);
          public          postgres    false    239            A           0    0    auth_user_groups_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);
          public          postgres    false    247            B           0    0    auth_user_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.auth_user_id_seq', 1, false);
          public          postgres    false    245            C           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);
          public          postgres    false    249            D           0    0    django_admin_log_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);
          public          postgres    false    251            E           0    0    django_content_type_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.django_content_type_id_seq', 14, true);
          public          postgres    false    237            F           0    0    django_migrations_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_migrations_id_seq', 20, true);
          public          postgres    false    235            G           0    0 #   gbl_function_master_function_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.gbl_function_master_function_id_seq', 23, true);
          public          postgres    false    217            H           0    0    gbl_masterdata_master_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.gbl_masterdata_master_id_seq', 27, true);
          public          postgres    false    223            I           0    0    gbl_module_master_module_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.gbl_module_master_module_id_seq', 5, true);
          public          postgres    false    215            J           0    0    gbl_users_user_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.gbl_users_user_id_seq', 1, false);
          public          postgres    false    219            K           0    0     plant_config_plant_config_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.plant_config_plant_config_id_seq', 33, true);
          public          postgres    false    227            L           0    0 )   plant_config_product_plant_product_id_seq    SEQUENCE SET     Y   SELECT pg_catalog.setval('public.plant_config_product_plant_product_id_seq', 242, true);
          public          postgres    false    272            M           0    0 +   plant_config_workshop_plant_workshop_id_seq    SEQUENCE SET     [   SELECT pg_catalog.setval('public.plant_config_workshop_plant_workshop_id_seq', 124, true);
          public          postgres    false    270            N           0    0 +   plant_function_master_plant_function_id_seq    SEQUENCE SET     [   SELECT pg_catalog.setval('public.plant_function_master_plant_function_id_seq', 808, true);
          public          postgres    false    274            O           0    0    plant_master_plant_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.plant_master_plant_id_seq', 1, false);
          public          postgres    false    225            P           0    0    plant_role_role_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.plant_role_role_id_seq', 1, false);
          public          postgres    false    221            Q           0    0     plant_user_role_user_role_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.plant_user_role_user_role_id_seq', 1, false);
          public          postgres    false    231            R           0    0    plant_users_plant_user_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.plant_users_plant_user_id_seq', 1, false);
          public          postgres    false    229            S           0    0 &   role_permission_role_permission_id_seq    SEQUENCE SET     U   SELECT pg_catalog.setval('public.role_permission_role_permission_id_seq', 1, false);
          public          postgres    false    233            $           2606    17658    app_currency app_currency_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.app_currency
    ADD CONSTRAINT app_currency_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.app_currency DROP CONSTRAINT app_currency_pkey;
       public            postgres    false    254            &           2606    17664    app_erp app_erp_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.app_erp
    ADD CONSTRAINT app_erp_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.app_erp DROP CONSTRAINT app_erp_pkey;
       public            postgres    false    256            (           2606    17670    app_function app_function_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.app_function
    ADD CONSTRAINT app_function_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.app_function DROP CONSTRAINT app_function_pkey;
       public            postgres    false    258            *           2606    17676    app_language app_language_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.app_language
    ADD CONSTRAINT app_language_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.app_language DROP CONSTRAINT app_language_pkey;
       public            postgres    false    260            ,           2606    17682 $   app_plantconfig app_plantconfig_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.app_plantconfig
    ADD CONSTRAINT app_plantconfig_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.app_plantconfig DROP CONSTRAINT app_plantconfig_pkey;
       public            postgres    false    262            .           2606    17688    app_product app_product_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.app_product
    ADD CONSTRAINT app_product_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.app_product DROP CONSTRAINT app_product_pkey;
       public            postgres    false    264            0           2606    17694    app_timezone app_timezone_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.app_timezone
    ADD CONSTRAINT app_timezone_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.app_timezone DROP CONSTRAINT app_timezone_pkey;
       public            postgres    false    266            2           2606    17700    app_unit app_unit_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.app_unit
    ADD CONSTRAINT app_unit_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.app_unit DROP CONSTRAINT app_unit_pkey;
       public            postgres    false    268                       2606    17707    auth_group auth_group_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public            postgres    false    242            
           2606    17584 R   auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
 |   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
       public            postgres    false    244    244                       2606    17553 2   auth_group_permissions auth_group_permissions_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public            postgres    false    244                       2606    17545    auth_group auth_group_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public            postgres    false    242                        2606    17575 F   auth_permission auth_permission_content_type_id_codename_01ab375a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
 p   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
       public            postgres    false    240    240                       2606    17539 $   auth_permission auth_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public            postgres    false    240                       2606    17567 &   auth_user_groups auth_user_groups_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
       public            postgres    false    248                       2606    17599 @   auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);
 j   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
       public            postgres    false    248    248                       2606    17559    auth_user auth_user_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
       public            postgres    false    246                       2606    17573 :   auth_user_user_permissions auth_user_user_permissions_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
       public            postgres    false    250                       2606    17613 Y   auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
       public            postgres    false    250    250                       2606    17702     auth_user auth_user_username_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);
 J   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
       public            postgres    false    246            !           2606    17634 &   django_admin_log django_admin_log_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public            postgres    false    252            �           2606    17533 E   django_content_type django_content_type_app_label_model_76bd3d3b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
 o   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
       public            postgres    false    238    238            �           2606    17531 ,   django_content_type django_content_type_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public            postgres    false    238            �           2606    17525 (   django_migrations django_migrations_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
       public            postgres    false    236            5           2606    17715 "   django_session django_session_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
 L   ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
       public            postgres    false    269            �           2606    17353 ,   gbl_function_master gbl_function_master_pkey 
   CONSTRAINT     s   ALTER TABLE ONLY public.gbl_function_master
    ADD CONSTRAINT gbl_function_master_pkey PRIMARY KEY (function_id);
 V   ALTER TABLE ONLY public.gbl_function_master DROP CONSTRAINT gbl_function_master_pkey;
       public            postgres    false    218            �           2606    17387 "   gbl_masterdata gbl_masterdata_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public.gbl_masterdata
    ADD CONSTRAINT gbl_masterdata_pkey PRIMARY KEY (master_id);
 L   ALTER TABLE ONLY public.gbl_masterdata DROP CONSTRAINT gbl_masterdata_pkey;
       public            postgres    false    224            �           2606    17344 (   gbl_module_master gbl_module_master_pkey 
   CONSTRAINT     m   ALTER TABLE ONLY public.gbl_module_master
    ADD CONSTRAINT gbl_module_master_pkey PRIMARY KEY (module_id);
 R   ALTER TABLE ONLY public.gbl_module_master DROP CONSTRAINT gbl_module_master_pkey;
       public            postgres    false    216            �           2606    17368    gbl_users gbl_users_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.gbl_users
    ADD CONSTRAINT gbl_users_pkey PRIMARY KEY (user_id);
 B   ALTER TABLE ONLY public.gbl_users DROP CONSTRAINT gbl_users_pkey;
       public            postgres    false    220            �           2606    17405    plant_config plant_config_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.plant_config
    ADD CONSTRAINT plant_config_pkey PRIMARY KEY (plant_config_id);
 H   ALTER TABLE ONLY public.plant_config DROP CONSTRAINT plant_config_pkey;
       public            postgres    false    228            <           2606    17743 .   plant_config_product plant_config_product_pkey 
   CONSTRAINT     z   ALTER TABLE ONLY public.plant_config_product
    ADD CONSTRAINT plant_config_product_pkey PRIMARY KEY (plant_product_id);
 X   ALTER TABLE ONLY public.plant_config_product DROP CONSTRAINT plant_config_product_pkey;
       public            postgres    false    273            8           2606    17729 0   plant_config_workshop plant_config_workshop_pkey 
   CONSTRAINT     }   ALTER TABLE ONLY public.plant_config_workshop
    ADD CONSTRAINT plant_config_workshop_pkey PRIMARY KEY (plant_workshop_id);
 Z   ALTER TABLE ONLY public.plant_config_workshop DROP CONSTRAINT plant_config_workshop_pkey;
       public            postgres    false    271            @           2606    17810 0   plant_function_master plant_function_master_pkey 
   CONSTRAINT     }   ALTER TABLE ONLY public.plant_function_master
    ADD CONSTRAINT plant_function_master_pkey PRIMARY KEY (plant_function_id);
 Z   ALTER TABLE ONLY public.plant_function_master DROP CONSTRAINT plant_function_master_pkey;
       public            postgres    false    275            �           2606    17396    plant_master plant_master_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.plant_master
    ADD CONSTRAINT plant_master_pkey PRIMARY KEY (plant_id);
 H   ALTER TABLE ONLY public.plant_master DROP CONSTRAINT plant_master_pkey;
       public            postgres    false    226            �           2606    17378    plant_role plant_role_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.plant_role
    ADD CONSTRAINT plant_role_pkey PRIMARY KEY (role_id);
 D   ALTER TABLE ONLY public.plant_role DROP CONSTRAINT plant_role_pkey;
       public            postgres    false    222            �           2606    17438 $   plant_user_role plant_user_role_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.plant_user_role
    ADD CONSTRAINT plant_user_role_pkey PRIMARY KEY (user_role_id);
 N   ALTER TABLE ONLY public.plant_user_role DROP CONSTRAINT plant_user_role_pkey;
       public            postgres    false    232            �           2606    17419    plant_users plant_users_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.plant_users
    ADD CONSTRAINT plant_users_pkey PRIMARY KEY (plant_user_id);
 F   ALTER TABLE ONLY public.plant_users DROP CONSTRAINT plant_users_pkey;
       public            postgres    false    230            �           2606    17461 $   role_permission role_permission_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.role_permission
    ADD CONSTRAINT role_permission_pkey PRIMARY KEY (role_permission_id);
 N   ALTER TABLE ONLY public.role_permission DROP CONSTRAINT role_permission_pkey;
       public            postgres    false    234            >           2606    17749 ,   plant_config_product uc_plant_config_product 
   CONSTRAINT     ~   ALTER TABLE ONLY public.plant_config_product
    ADD CONSTRAINT uc_plant_config_product UNIQUE (plant_config_id, product_id);
 V   ALTER TABLE ONLY public.plant_config_product DROP CONSTRAINT uc_plant_config_product;
       public            postgres    false    273    273            :           2606    17747 .   plant_config_workshop uc_plant_config_workshop 
   CONSTRAINT     �   ALTER TABLE ONLY public.plant_config_workshop
    ADD CONSTRAINT uc_plant_config_workshop UNIQUE (plant_config_id, workshop_id);
 X   ALTER TABLE ONLY public.plant_config_workshop DROP CONSTRAINT uc_plant_config_workshop;
       public            postgres    false    271    271            B           2606    17822 +   plant_function_master unique_plant_function 
   CONSTRAINT     �   ALTER TABLE ONLY public.plant_function_master
    ADD CONSTRAINT unique_plant_function UNIQUE (plant_id, module_id, function_id);
 U   ALTER TABLE ONLY public.plant_function_master DROP CONSTRAINT unique_plant_function;
       public            postgres    false    275    275    275                       1259    17708    auth_group_name_a6ea08ec_like    INDEX     h   CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.auth_group_name_a6ea08ec_like;
       public            postgres    false    242                       1259    17595 (   auth_group_permissions_group_id_b120cbf9    INDEX     o   CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
 <   DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
       public            postgres    false    244                       1259    17596 -   auth_group_permissions_permission_id_84c5c92e    INDEX     y   CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
 A   DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
       public            postgres    false    244            �           1259    17581 (   auth_permission_content_type_id_2f476e4b    INDEX     o   CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
 <   DROP INDEX public.auth_permission_content_type_id_2f476e4b;
       public            postgres    false    240                       1259    17611 "   auth_user_groups_group_id_97559544    INDEX     c   CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);
 6   DROP INDEX public.auth_user_groups_group_id_97559544;
       public            postgres    false    248                       1259    17610 !   auth_user_groups_user_id_6a12ed8b    INDEX     a   CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);
 5   DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
       public            postgres    false    248                       1259    17625 1   auth_user_user_permissions_permission_id_1fbb5f2c    INDEX     �   CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);
 E   DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
       public            postgres    false    250                       1259    17624 +   auth_user_user_permissions_user_id_a95ead1b    INDEX     u   CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);
 ?   DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
       public            postgres    false    250                       1259    17703     auth_user_username_6821ab7c_like    INDEX     n   CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);
 4   DROP INDEX public.auth_user_username_6821ab7c_like;
       public            postgres    false    246                       1259    17645 )   django_admin_log_content_type_id_c4bce8eb    INDEX     q   CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
 =   DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
       public            postgres    false    252            "           1259    17646 !   django_admin_log_user_id_c564eba6    INDEX     a   CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
 5   DROP INDEX public.django_admin_log_user_id_c564eba6;
       public            postgres    false    252            3           1259    17717 #   django_session_expire_date_a5c62663    INDEX     e   CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
 7   DROP INDEX public.django_session_expire_date_a5c62663;
       public            postgres    false    269            6           1259    17716 (   django_session_session_key_c0390e0f_like    INDEX     ~   CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
 <   DROP INDEX public.django_session_session_key_c0390e0f_like;
       public            postgres    false    269            L           2606    17590 O   auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
       public          postgres    false    240    244    4866            M           2606    17585 P   auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
       public          postgres    false    244    4871    242            K           2606    17576 E   auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
       public          postgres    false    4861    240    238            N           2606    17605 D   auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 n   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
       public          postgres    false    242    248    4871            O           2606    17600 B   auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
       public          postgres    false    246    248    4879            P           2606    17619 S   auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 }   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
       public          postgres    false    250    4866    240            Q           2606    17614 V   auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
       public          postgres    false    250    4879    246            R           2606    17635 G   django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
       public          postgres    false    4861    238    252            S           2606    17640 B   django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
       public          postgres    false    246    252    4879            C           2606    17354 6   gbl_function_master gbl_function_master_module_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.gbl_function_master
    ADD CONSTRAINT gbl_function_master_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.gbl_module_master(module_id);
 `   ALTER TABLE ONLY public.gbl_function_master DROP CONSTRAINT gbl_function_master_module_id_fkey;
       public          postgres    false    4837    218    216            D           2606    17406 '   plant_config plant_config_plant_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plant_config
    ADD CONSTRAINT plant_config_plant_id_fkey FOREIGN KEY (plant_id) REFERENCES public.plant_master(plant_id);
 Q   ALTER TABLE ONLY public.plant_config DROP CONSTRAINT plant_config_plant_id_fkey;
       public          postgres    false    226    228    4847            T           2606    17730 @   plant_config_workshop plant_config_workshop_plant_config_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plant_config_workshop
    ADD CONSTRAINT plant_config_workshop_plant_config_id_fkey FOREIGN KEY (plant_config_id) REFERENCES public.plant_config(plant_config_id);
 j   ALTER TABLE ONLY public.plant_config_workshop DROP CONSTRAINT plant_config_workshop_plant_config_id_fkey;
       public          postgres    false    228    4849    271            U           2606    17816 <   plant_function_master plant_function_master_function_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plant_function_master
    ADD CONSTRAINT plant_function_master_function_id_fkey FOREIGN KEY (function_id) REFERENCES public.gbl_function_master(function_id);
 f   ALTER TABLE ONLY public.plant_function_master DROP CONSTRAINT plant_function_master_function_id_fkey;
       public          postgres    false    4839    275    218            V           2606    17811 9   plant_function_master plant_function_master_plant_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plant_function_master
    ADD CONSTRAINT plant_function_master_plant_id_fkey FOREIGN KEY (plant_id) REFERENCES public.plant_master(plant_id);
 c   ALTER TABLE ONLY public.plant_function_master DROP CONSTRAINT plant_function_master_plant_id_fkey;
       public          postgres    false    4847    275    226            G           2606    17439 2   plant_user_role plant_user_role_plant_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plant_user_role
    ADD CONSTRAINT plant_user_role_plant_user_id_fkey FOREIGN KEY (plant_user_id) REFERENCES public.plant_users(plant_user_id);
 \   ALTER TABLE ONLY public.plant_user_role DROP CONSTRAINT plant_user_role_plant_user_id_fkey;
       public          postgres    false    4851    232    230            H           2606    17444 ,   plant_user_role plant_user_role_role_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plant_user_role
    ADD CONSTRAINT plant_user_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.plant_role(role_id);
 V   ALTER TABLE ONLY public.plant_user_role DROP CONSTRAINT plant_user_role_role_id_fkey;
       public          postgres    false    4843    222    232            E           2606    17420 %   plant_users plant_users_plant_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plant_users
    ADD CONSTRAINT plant_users_plant_id_fkey FOREIGN KEY (plant_id) REFERENCES public.plant_master(plant_id);
 O   ALTER TABLE ONLY public.plant_users DROP CONSTRAINT plant_users_plant_id_fkey;
       public          postgres    false    226    4847    230            F           2606    17425 $   plant_users plant_users_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plant_users
    ADD CONSTRAINT plant_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.gbl_users(user_id);
 N   ALTER TABLE ONLY public.plant_users DROP CONSTRAINT plant_users_user_id_fkey;
       public          postgres    false    4841    220    230            I           2606    17467 -   role_permission role_permission_plant_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.role_permission
    ADD CONSTRAINT role_permission_plant_id_fkey FOREIGN KEY (plant_id) REFERENCES public.plant_master(plant_id);
 W   ALTER TABLE ONLY public.role_permission DROP CONSTRAINT role_permission_plant_id_fkey;
       public          postgres    false    226    234    4847            J           2606    17462 ,   role_permission role_permission_role_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.role_permission
    ADD CONSTRAINT role_permission_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.plant_role(role_id);
 V   ALTER TABLE ONLY public.role_permission DROP CONSTRAINT role_permission_role_id_fkey;
       public          postgres    false    4843    234    222                  x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �      �   %  x�]�[n�0E��U��Q̣��F��E;�c��~L=\U�a�A>�����o�����c�������ϼ����oi���- ��W▀-��c�k�}C����q���qJ�5��'-g@�S�Y��{EC����rX�mv³oZ���EH�N��!��0 4n�����kA`����Ӕ�G�ӧ@�#p��iG��\N��Z_st�־��E�`2�U{x��|�&�t��3�zaZ���]�,�I�`�W0�u��� ��~[����;����&���+�ɸ��
��0��I��2�H�'ߘd�T`lR�c��J4�XI���ԯ�u]�X^�ƤZQ$ �I�IE@�r���@��G>g�����־19�We!M�5�]�d���9,�BI�缹���8��]{��[��#ͭ�_0I?��թ_P�?�؟V=�L��_]��ǥom�Į��~����.�1#�_ǟX��R�u,�}c_��|�#5A�aP�T}A�T�1�*���;[�4���6?\�@��9v�>����]�x            x������ � �            x������ � �      	      x������ � �            x������ � �      �   �   x�M�K�0е}D���(uC�։{QNOH��n��#;����Uv�����l�֔ǣ����t�*	^ d�6ӽP�^�R_�_��R �q���IR���b�{��ݫ�h>:�]Z��Œ"��$��ةi�w涘�����ٝKR      �   �  x���ݎ� �������L(@~�Y6��q2����Hw2n�����:��.�d}J��.!�y��J(!��%o�}c��B��l7ژ5�����h������*&9Q���CEqC�8�0�)|Z�U4}�ђ*U0���,E�%<^G3`�\��8���d�����y'�IP{�r�P����nh����+a4~X�`q�W)�su�1�k������>-��鲏��,��*/p{��L�4�(���5i�fL6�l��e+x#�d�p�~�_�����c�.y��q�)IqM�N�J�Ϥm���t��$��=xLr��͒�1q��u<WR
d7X�����b���ns8�v?Y�+G��>��z�B\��jc'�,yT�Ӣ�JW��JT�N��.��LT����Oh
��4�Ӏ��:���A�:�� �9�e���u{�c��RV��}n���O�ӌ���$�b�ާ�
Z�"��z�\���f            x������ � �      �   V  x����n�0�g�)<U� ��� A�E��V]X\�T���q���=�2�R�H���\��F�p�<��t�Q�My>eِ%y�'��>JY�
��pr�:#$Х�ന�EF	��24͔�^C?�Ŏ��U��M��?���:F���(�-^����}����y����,Füm�݂�eRj)��&@�HBA�~������\Z�/PmbH�P�JK��P�&�e��W�7"�q<3#�]�r���.���� v�l�g�z�!�B�*x�����������`�Y��>N2̊�
�;�d�uS���`U��>kᘏB:��<��,�6��U�l�Q�%�`�      �   
  x���ݎ�@���)�nk?(���6{3� �S2m׬����N_b}���n�ho<�BC���9�9�HΒx'���y�ŚƏy��>$E�۴{]��Z}j[#����Cρ;��1;�L���i��"��и`��$��ij���w��`ˬT�ŵjG��/�m���5~~���������N���z��������h�⌻q��6�;�
�8]�ʃḵ��f�#�U��<#\�"$�l��\�O%�`}���U����:k���9]��O_1�MލÛt|�@������ӄ�#S�p�	O5WkL�%�l�-i��.5ݑi^р�HjEq����%�K��I���k݇'I��_�{mݫ�9�q�ą���A�/�Zla�]���_Q���5�9r�\b���c;5�{~V��b�φ���0���v��M�F��7�e���~Bb!a��i���Nyx�1)K�^T��g���j��~�o�m���ϝ��rL�;��s���N����      �   {   x�3�-N-Rp��+)��QpLNN-.���,@dd`d�k`�kh�`hjehdeb�gajlib��2��M,.��X�H�6cN���T���|Ҭ3�J-�/*!A�	�Ob��c^bNeq&	�b���� .�C       �      x������ � �      �      x������ � �             x������ � �            x������ � �      "      x������ � �      �   A   x�3400�tJ-K-ʩ�,��!##]C]C##+C+C=s#K�lh���!W� ��=      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �     