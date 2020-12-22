create or replace function valid_check()
    returns trigger
as $$
    declare
        address_code varchar;
        city varchar;
        province varchar;
        address varchar;
        birthday varchar;
        checksum int;
        origin_cs int;
    begin

        --address
        address_code := substring(new.id, 1, 6);
        select name into address
        from district
        where code = address_code;
        if address is null
        then
            raise exception 'invalid address code';
        else
            if substring(address_code, 3, 4) = '0000'
            then
                new.address := address;
            elseif substring(address_code, 5, 2) = '00'
            then
                select name into province
                from district where code = substring(address_code, 1, 2) || '0000';
                new.address := province || ',' || address;
            else
                select name into province
                from district where code = substring(address_code, 1, 2) || '0000';
                select name into city
                from district where code = substring(address_code, 1, 4) || '00';
                if city is not null
                then
                    new.address := province || ',' || city || ',' || address;
                else
                    new.address := province || ',' || address;
                end if;
            end if;
        end if;

        --birthday
        select to_char(to_date(substring(new.id, 7, 8), 'yyyyMMdd'), 'yyyyMMdd') into birthday;
            new.birthday := birthday;
        end if;

        --checksum
        checksum := 0;
        for i in 1 .. 17 loop
            checksum := checksum + (mod(pow(2,18-i)::integer, 11) * substring(new.id, i, 1)::integer);
        end loop;
        checksum := mod(12 - mod(checksum, 11), 11);
        if substring(new.id, 18, 1) = 'X'
        then
            origin_cs := 10;
        else
            origin_cs := substring(new.id, 18, 1)::integer;
        end if;
        if origin_cs <> checksum
        then
            raise exception 'wrong checksum';
        end if;
        return new;
    end;
    $$
language plpgsql;