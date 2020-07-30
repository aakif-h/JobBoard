class UserLib {

    static getReqAttrAndTypes(){
        return {"username": "string", "password": "string", "user_type": "number", "company_id": "number"}
    }


    static async create(user_type,username,password,company_id) {
        // verify parameters and create data to send to the route
        const arrayOfAttributes = 'user_type,username,password,company_id'.split(',');
        let routeGroupObj = {};
        for (let i = 0; i < arguments.length; i++) {
            if (
                typeof arguments[i] !==
                UserLib.getReqAttrAndTypes()[arrayOfAttributes[i]]
            ) {
                throw `${arrayOfAttributes[i]} expects ${UserLib.getReqAttrAndTypes()[arrayOfAttributes[i]]}, but recieved ${typeof arguments[i]}`;
            }
            routeGroupObj[arrayOfAttributes[i]] = arguments[i];
        }
        // Create and set id property to 0, currently required for the route
        routeGroupObj.appToken = "15af2548-c22e-46cb-b07f-5a8ef74d90a0";

        // request to server
        let resStream = await fetch(`/createUser`, {
            method: 'POST',
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(routeGroupObj),
        })
        .catch((err) => {
            console.log('Error:', err)
            return false;
        });

        let res = await resStream.json();

        return {
            createdObj: res,
            status: resStream.status === 200
        };
    }


    static async read(attributes_dict){
        for (const [attr_name, attr_val] of Object.entries(attributes_dict)) {
            if (typeof attr_val !== UserLib.getReqAttrAndTypes()[attr_name]) {
                throw "Bad Params! [Attribute Type Error]";
            }
        }
        let result_stream = await fetch(`/readUser`, {
            method: 'POST',
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify("appToken":"15af2548-c22e-46cb-b07f-5a8ef74d90a0", "filters":attributes_dict)
        })
        .catch((err) => {
            console.log('Error: ', err);
            return false;
        });
        let res = await result_stream.json();

        return {
            readedObj:res,
            status:result_stream.status === 200
        };
    }


    static async update(id, attributes_dict) {
        for (const [attr_name, attr_val] of Object.entries(attributes_dict)) {
            if(!UserLib.getReqAttrAndTypes()[attr_name])
                throw `${attr_name} is not an attribute of User`;

            if (typeof attr_val !== UserLib.getReqAttrAndTypes()[attr_name]) {
                throw `[Attribute Type Error] ${attr_name} expected ${UserLib.getReqAttrAndTypes()[attr_name]}, but received ${typeof attr_val}`;
            }
        }
        const updateAttributes = {};
        updateAttributes["id"] = id;
        updateAttributes["data"] = attributes_dict
        attributes_dict.appToken = "15af2548-c22e-46cb-b07f-5a8ef74d90a0";
        let result_stream = await fetch(`/updateUser`, {
            method: 'POST',
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(updateAttributes)
        })
        .catch((err) => {
            console.log('Error: ', err);
            return false;
        });
        return result_stream.status === 200;
    }


    static async delete(id){
        if(typeof(id) !== "number") throw `[Attribute Type Error] ID expected of type 'number', but received of type ${typeof id}`;

        let resStream = await fetch(`/deleteUser`,{
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({id, appToken:"15af2548-c22e-46cb-b07f-5a8ef74d90a0"})
        })
        .catch((err) => {
            console.log('Error: ', err);
            return false;
        });
        return resStream.status===200;
    }

}
