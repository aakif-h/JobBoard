class JobLib {

    static getReqAttrAndTypes(){
        return {"user_id": "number", "description": "string", "number_applicants": "number", "title": "string", "company_id": "number", "job_link": "string"}
    }


    static async create(title,user_id,company_id,job_link,number_applicants,description) {
        // verify parameters and create data to send to the route
        const arrayOfAttributes = 'title,user_id,company_id,job_link,number_applicants,description'.split(',');
        let routeGroupObj = {};
        for (let i = 0; i < arguments.length; i++) {
            if (
                typeof arguments[i] !==
                JobLib.getReqAttrAndTypes()[arrayOfAttributes[i]]
            ) {
                throw `${arrayOfAttributes[i]} expects ${JobLib.getReqAttrAndTypes()[arrayOfAttributes[i]]}, but recieved ${typeof arguments[i]}`;
            }
            routeGroupObj[arrayOfAttributes[i]] = arguments[i];
        }
        // Create and set id property to 0, currently required for the route
        routeGroupObj.appToken = "15af2548-c22e-46cb-b07f-5a8ef74d90a0";

        // request to server
        let resStream = await fetch(`/createJob`, {
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
            if (typeof attr_val !== JobLib.getReqAttrAndTypes()[attr_name]) {
                throw "Bad Params! [Attribute Type Error]";
            }
        }
        let result_stream = await fetch(`/readJob`, {
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
            if(!JobLib.getReqAttrAndTypes()[attr_name])
                throw `${attr_name} is not an attribute of Job`;

            if (typeof attr_val !== JobLib.getReqAttrAndTypes()[attr_name]) {
                throw `[Attribute Type Error] ${attr_name} expected ${JobLib.getReqAttrAndTypes()[attr_name]}, but received ${typeof attr_val}`;
            }
        }
        const updateAttributes = {};
        updateAttributes["id"] = id;
        updateAttributes["data"] = attributes_dict
        attributes_dict.appToken = "15af2548-c22e-46cb-b07f-5a8ef74d90a0";
        let result_stream = await fetch(`/updateJob`, {
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

        let resStream = await fetch(`/deleteJob`,{
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
